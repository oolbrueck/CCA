import re
import matplotlib.pyplot as plt
import numpy as np
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Protocol import protocol_obj


class SnippetGenerator:

    def __init__(self, neighboring_files, domain_window_size, co_domain_window_size, current_file, cursor_position, compare_method, intersection_threshold, value_threshold):
        self.neighboring_files = neighboring_files
        self.domain_window_size = domain_window_size
        self.co_domain_window_size = co_domain_window_size
        self.current_file = current_file
        self.cursor_position = cursor_position
        self.compare_method = compare_method
        self.intersection_threshold = intersection_threshold
        self.value_threshold = value_threshold

    def get_snippets(self):
        domain_window_code = self.__get_code_from_domain_window()

        union_of_all_files = (self.neighboring_files['file_related_to_parent_class'] +
                              self.neighboring_files['files_related_to_siblings_classes'] +
                              self.neighboring_files['file_related_to_imported_classes'] +
                              self.neighboring_files['file_related_to_classes_from_neighboring_files'])

        filtered_windows_of_all_files = []

        if len(union_of_all_files) < 20:
            warnings.warn("Es konnten nicht genügend Dateien gefunden werden, um den Kontext zu simulieren.")
            protocol_obj.is_valid = False

        for file_path in union_of_all_files:
            sliding_windows = self.__get_sliding_windows(file_path)
            windows_of_specific_file = []

            # Für jedes Sliding Window wird die ähnlichkeit mit dem Bereich um den Cursor (Domain Window) berechnet
            for sliding_window in sliding_windows:
                if self.compare_method == "jaccard":
                    value = self.__calculate_jaccard_value(domain_window_code, sliding_window.get('code'))
                elif self.compare_method == "cosine":
                    value = self.__calculate_cosine_value(domain_window_code, sliding_window.get('code'))
                elif self.compare_method == "levenshtein":
                    value = self.__calculate_levenshtein_value(domain_window_code, sliding_window.get('code'))
                else:
                    warnings.warn("No valid compare_method selected")
                    protocol_obj.is_valid = False
                    return

                window = {
                    'file_path': file_path,
                    'file_category': self.__get_file_category(file_path),
                    'range': sliding_window.get('range'),
                    'value': value,
                    'code': sliding_window.get('code')
                }
                # Zunächst werden alle Sliding Windows des Files mit nützlichen Informationen angereichert und gesammelt
                windows_of_specific_file.append(window)

            # Da man nur solche Sliding Windows benötigt, die einen bestimmten Schwellenwert erfüllen und sich nicht
            # überschneiden, werden die Sliding Windows gefiltert
            filtered_windows_of_specific_file = self.__filter_windows_of_specific_file(windows_of_specific_file)
            # und anschließend der Sammlung 'fertigen' Sliding Windows hinzugefügt
            filtered_windows_of_all_files.extend(filtered_windows_of_specific_file)

        # for window in filtered_windows_of_all_files:
        #     print(f"file_path: {window['file_path']}, file_category: {window['file_category']}, range: {window['range']}, value: {window['value']}")
        #
        # self.__print_plot(filtered_windows_of_all_files, '')

        protocol_obj.filtered_windows_of_all_files = filtered_windows_of_all_files
        return filtered_windows_of_all_files

    def __tokenize_code(self, code):
        tokens = re.findall(r"[\w']+|[(){}[\],.;]", code)
        return tokens

    # Die Aufgabe der Funktion liegt darin den Code zurückzugeben, der sich über und unter der Stelle befindet, wo neuer Code
    # eingefügt werden soll, also am Cursor. Es werden self.domain_window_size viele - nicht leere - Zeilen zurückgegeben.
    def __get_code_from_domain_window(self):
        with open(self.current_file, 'r') as f:
            code = f.read()
        lines = code.split("\n")
        lines[self.cursor_position - 1] += "<curser>"
        lines = [line for line in lines if line.strip()]

        cursor_position_after_removing_empty_lines = [i for i, line in enumerate(lines) if "<curser>" in line][0]
        modified_lines = [line + "\n" for line in lines]
        domain_window = "".join(modified_lines[cursor_position_after_removing_empty_lines - int(self.domain_window_size / 2):
                                               cursor_position_after_removing_empty_lines + 1 + int(self.domain_window_size / 2)])
        domain_window = domain_window.replace("<curser>", "")

        protocol_obj.domain_window = domain_window
        return domain_window

    # Die Funktion gibt eine Liste von Sliding Windows zurück, die sich über den gesamten Code des übergebenen Files erstrecken.
    # Das einzelne window-Objekt enthält sowohl den Code als auch den Bereich, in dem sich der Code befindet.
    def __get_sliding_windows(self, file_path):
        with open(file_path, 'r') as f:
            code = f.read()
        lines = code.split("\n")
        sliding_windows = []
        for i in range(0, len(lines) - self.co_domain_window_size):
            window = {
                'code': "".join([line + "\n" for line in lines[i:i + self.co_domain_window_size]]),
                'range': [i, i + self.co_domain_window_size]
            }
            sliding_windows.append(window)
        return sliding_windows

    def __get_file_category(self, file_path):
        if file_path in self.neighboring_files['file_related_to_parent_class']:
            return 'file_related_to_parent_class'
        elif file_path in self.neighboring_files['files_related_to_siblings_classes']:
            return 'files_related_to_siblings_classes'
        elif file_path in self.neighboring_files['file_related_to_imported_classes']:
            return 'file_related_to_imported_classes'
        elif file_path in self.neighboring_files['file_related_to_classes_from_neighboring_files']:
            return 'file_related_to_classes_from_neighboring_files'
        else:
            return 'unknown'

    # Funktion filtert die Sliding Windows anhand der Schwellenwerte und der Schnittmenge
    def __filter_windows_of_specific_file(self, windows_of_specific_file):
        threshold_fulfilling_windows = [window for window in windows_of_specific_file if window['value'] > self.value_threshold]
        threshold_fulfilling_windows.sort(key=lambda x: x['value'], reverse=True)

        threshold_not_fulfilling_windows = [window for window in windows_of_specific_file if window['value'] < self.value_threshold]
        protocol_obj.threshold_not_fulfilling_windows = threshold_not_fulfilling_windows

        # Die Range (Start-Zeile, End-Zeile) wird in eine Menge von Zahlen umgewndelt, um die Schnittmenge
        # mit anderen Sliding Windows einfacher zu berechnen
        for window in threshold_fulfilling_windows:
            window['range'] = list(range(window['range'][0], window['range'][1]))

        disjunct_windows = []
        if threshold_fulfilling_windows:
            disjunct_windows.append(threshold_fulfilling_windows[0])

        for window in threshold_fulfilling_windows[1:]:
            range_sequence_of_window = set(window['range'])
            not_add_due_to_intersection = False
            for filtered_window in disjunct_windows:
                range_sequence_of_filtered_window = set(filtered_window['range'])
                intersection_value = len(range_sequence_of_window.intersection(range_sequence_of_filtered_window))
                proportion = intersection_value / self.co_domain_window_size
                if proportion > self.intersection_threshold:
                    not_add_due_to_intersection = True
                    break
            if not not_add_due_to_intersection:
                disjunct_windows.append(window)

        for window in disjunct_windows:
            window['range'] = [window['range'][0], window['range'][-1]]

        protocol_obj.disjunct_windows = disjunct_windows
        return disjunct_windows

    def __calculate_jaccard_value(self, domain_window, sliding_window):
        domain_window_tokenized = self.__tokenize_code(domain_window)
        sliding_window_tokenized = self.__tokenize_code(sliding_window)
        intersection = len(set(domain_window_tokenized).intersection(sliding_window_tokenized))
        union = len(set(domain_window_tokenized).union(sliding_window_tokenized))
        jaccard_value = intersection / union
        return jaccard_value

    def __calculate_cosine_value(self, domain_window, sliding_window):
        domain_window_tokenized = self.__tokenize_code(domain_window)
        sliding_window_tokenized = self.__tokenize_code(sliding_window)

        sentence1 = ' '.join(domain_window_tokenized)
        sentence2 = ' '.join(sliding_window_tokenized)

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([sentence1, sentence2])

        similarity = cosine_similarity(vectors)

        return similarity[0, 1]

    def __calculate_levenshtein_value(self, domain_window_code, sliding_window):
        lines1 = domain_window_code.splitlines()
        lines2 = sliding_window.splitlines()
        m, n = len(lines1), len(lines2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if lines1[i - 1] == lines2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + 1)

        return dp[m][n]

    def __print_plot(self, windows_of_specific_file, file_path):
        print("plo")
        # Extracting ranges, values, and file paths
        x_ranges = [window['range'] for window in windows_of_specific_file]
        y_values = [window['value'] for window in windows_of_specific_file]
        file_names = [re.search(r'[^/\\]+$', window['file_path']).group() for window in windows_of_specific_file]

        repo_title_index = file_path.find("repos")
        if repo_title_index != -1:
            plot_title = file_path[repo_title_index:]
        else:
            plot_title = file_path

        # Generating a colormap
        colors = plt.cm.viridis(np.linspace(0, 1, len(x_ranges)))

        # Plotting the diagram with horizontal lines for ranges
        plt.figure(figsize=(10, 6))
        for i, (x_range, y_value, file_path_i) in enumerate(zip(x_ranges, y_values, file_names)):
            plt.hlines(y=y_value, xmin=x_range[0], xmax=x_range[1], color=colors[i], linewidth=2)
            plt.annotate(file_path_i, xy=(x_range[0], y_value), xytext=(5, 2), textcoords='offset points', fontsize=8,
                         color=colors[i])

        plt.xlabel('Range')
        plt.ylabel('Value')
        plt.title(f'{plot_title}')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
