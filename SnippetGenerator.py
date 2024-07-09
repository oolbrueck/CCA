import re
import matplotlib.pyplot as plt
import numpy as np
from pydantic import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SnippetGenerator:

    def __init__(self, neighboringFiles, domainWindowSize, coDomainWindowSize, currentFile, cursorPosition, compareMethod):
        self.neighboringFiles = neighboringFiles
        self.domainWindowSize = domainWindowSize
        self.coDomainWindowSize = coDomainWindowSize
        self.currentFile = currentFile
        self.cursorPosition = cursorPosition
        self.compareMethod = compareMethod

    def getSnippets(self):
        domainWindowCode = self.__getCodeFromDomainWindow()

        unionOfAllLists = (self.neighboringFiles['fileRelatedToParentClass'] +
                           self.neighboringFiles['filesRelatedToSiblingsClasses'] +
                           self.neighboringFiles['fileRelatedToImportedClasses'] +
                           self.neighboringFiles['fileRelatedToClassesFromNeighboringFiles'])

        filteredWindowsOfAllFiles = []

        print("unionOfAllLists: ", len(unionOfAllLists))

        for filePath in unionOfAllLists:
            slidingWindows = self.__getSlidingWindows(filePath)
            windowsOfSpecificFile = []

            for slidingWindow in slidingWindows:
                #switch case for compareMethod
                if self.compareMethod == "jaccard":
                    value = self.__calculateJaccardValue(domainWindowCode, slidingWindow.get('code'))
                elif self.compareMethod == "cosine":
                    value = self.__calculateCosineValue(domainWindowCode, slidingWindow.get('code'))
                elif self.compareMethod == "levenshtein":
                    value = self.__calculateLevenshteinValue(domainWindowCode, slidingWindow.get('code'))
                else:
                    warnings.warn("No valid compareMethod selected")
                    return
                window = {}
                window['filePath'] = filePath
                window['fileCategory'] = self.__getFileCategory(filePath)
                window['range'] = slidingWindow.get('range')
                window['value'] = value
                window['code'] = slidingWindow.get('code')

                windowsOfSpecificFile.append(window)

            filteredWindowsOfSpecificFile = self.__filterWindowsOfSpecificFile(windowsOfSpecificFile)

            filteredWindowsOfAllFiles.extend(filteredWindowsOfSpecificFile)

        for window in filteredWindowsOfAllFiles:
            print(f"filePath: {window['filePath']}, fileCategory: {window['fileCategory']}, range: {window['range']}, value: {window['value']}")

        self.__printPlot(filteredWindowsOfAllFiles, '')

        return filteredWindowsOfAllFiles

    def __tokenizeCode(self, code):
        # Regex zum Trennen von Tokens basierend auf Leerzeichen und speziellen Zeichen
        tokens = re.findall(r"[\w']+|[(){}[\],.;]", code)
        return tokens

    # Funktion liefert ein Code-Fenster um die aktuelle Cursor-Position
    # Das Fenster ist domainWindowSize + 1 groß, wobei Leerzeilen ignoriert werden
    def __getCodeFromDomainWindow(self):
        with open(self.currentFile, 'r') as f:
            code = f.read()
        lines = code.split("\n")
        line = lines[self.cursorPosition - 1] + "<curser>"
        lines[self.cursorPosition - 1] = line
        lines = [line for line in lines if line.strip()]  # Remove empty lines
        #get the line that contains the substring "<insert Code here>"
        cursorPositionAfterRemovingEmptyLines = [i for i, line in enumerate(lines) if "<curser>" in line][0]

        modified_lines = [line + "\n" for line in lines]
        domainWindow = "".join(modified_lines[cursorPositionAfterRemovingEmptyLines - int(self.domainWindowSize / 2):cursorPositionAfterRemovingEmptyLines + 1 + int(self.domainWindowSize / 2)])
        domainWindow = domainWindow.replace("<curser>", "")

        return domainWindow


    def __getSlidingWindows(self, filePath):
        with open(filePath, 'r') as f:
            code = f.read()
        lines = code.split("\n")
        slidingWindows = []
        for i in range(0, len(lines) - self.coDomainWindowSize):
            window = {}
            #join all lines in the window to a single string and append after each line a newline character
            window['code'] = "".join([line + "\n" for line in lines[i:i + self.coDomainWindowSize]])
            window['range'] = [i, i + self.coDomainWindowSize]
            slidingWindows.append(window)
        return slidingWindows

    def __getFileCategory(self, filePath):
        if filePath in self.neighboringFiles['fileRelatedToParentClass']:
            return 'fileRelatedToParentClass'
        elif filePath in self.neighboringFiles['filesRelatedToSiblingsClasses']:
            return 'filesRelatedToSiblingsClasses'
        elif filePath in self.neighboringFiles['fileRelatedToImportedClasses']:
            return 'fileRelatedToImportedClasses'
        elif filePath in self.neighboringFiles['fileRelatedToClassesFromNeighboringFiles']:
            return 'fileRelatedToClassesFromNeighboringFiles'
        else:
            return 'unknown'

    # Funktion dient dazu die Fenster herauszufiltern, welche einen Schwellenwert erfüllen und
    # gleichzeitig sich nicht zu stark überlappen
    def __filterWindowsOfSpecificFile(self, windowsOfSpecificFile):
        intersectionThreshold = 0.2
        valueThreshold = 0.2

        thresholdFulfillingWindows = [window for window in windowsOfSpecificFile if
                                      window['value'] > valueThreshold]
        thresholdFulfillingWindows.sort(key=lambda x: x['value'], reverse=True)

        for window in thresholdFulfillingWindows:  # Die beiden Zahlwerte in range werden zu einer Sequenz umgewandelt um später die Überschneidung zu berechnen
            window['range'] = list(range(window['range'][0], window['range'][1]))

        disjunctWindows = []  # inklusive disjunkte und fast disjunkte Windows (siehe intersectionThreshold)

        if len(thresholdFulfillingWindows) > 0:
            disjunctWindows.append(thresholdFulfillingWindows[
                                       0])  # Füge das erste Fenster hinzu, da es das Fenster mit dem höchsten value ist

        for window in thresholdFulfillingWindows[
                      1:]:  # Iteriere absteigend (bezogen auf value) über alle Fenster und füge sie hinzu
            rangeSequenceOfWindow = set(window['range'])  # wenn die Überschneidung nicht zu groß ist
            notAddDueToIntersection = False
            for filteredWindow in disjunctWindows:
                rangeSequenceOfFilteredWindow = set(filteredWindow['range'])
                intersectionValue = len(rangeSequenceOfWindow.intersection(rangeSequenceOfFilteredWindow))
                proportion = intersectionValue / self.coDomainWindowSize
                if proportion > intersectionThreshold:
                    notAddDueToIntersection = True
                    break
            if notAddDueToIntersection == False:
                disjunctWindows.append(window)

        for window in disjunctWindows:  # Die Sequenz wird wieder in ein Intervall umgewandelt
            window['range'] = [window['range'][0], window['range'][-1]]

        return disjunctWindows

    def __calculateJaccardValue(self, domainWindow, slidingWindow):
        domainWindowTokenized = self.__tokenizeCode(domainWindow)
        slidingWindowTokenized = self.__tokenizeCode(slidingWindow)
        intersection = len(set(domainWindowTokenized).intersection(slidingWindowTokenized))
        union = len(set(domainWindowTokenized).union(slidingWindowTokenized))
        jaccardValue = intersection / union
        return jaccardValue

    def __calculateCosineValue(self, domainWindow, slidingWindow):
        # Tokenisierung des Codes in Wörter
        domainWindowTokenized = self.__tokenizeCode(domainWindow)
        slidingWindowTokenized = self.__tokenizeCode(slidingWindow)

        # Zusammenfügen der Tokens zu Sätzen für TF-IDF
        sentence1 = ' '.join(domainWindowTokenized)
        sentence2 = ' '.join(slidingWindowTokenized)

        # TF-IDF Vektorisierung
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([sentence1, sentence2])

        # Berechnung der Kosinusähnlichkeit
        similarity = cosine_similarity(vectors)

        return similarity[0, 1]

    def __calculateLevenshteinValue(self, domainWindowCode, slidingWindow):
        # Split code into lines
        lines1 = domainWindowCode.splitlines()
        lines2 = slidingWindow.splitlines()
        m = len(lines1)
        n = len(lines2)

        # Initialize dp matrix
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base cases
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Fill dp matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if lines1[i - 1] == lines2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j] + 1,      # Delete operation
                                   dp[i][j - 1] + 1,      # Insert operation
                                   dp[i - 1][j - 1] + 1)  # Replace operation

        return dp[m][n]

    def __printPlot(self, windowsOfSpecificFile, filePath):
        print("plo")
        # Extracting ranges, values, and file paths
        x_ranges = [window['range'] for window in windowsOfSpecificFile]
        y_values = [window['value'] for window in windowsOfSpecificFile]
        file_names = [re.search(r'[^/\\]+$', window['filePath']).group() for window in windowsOfSpecificFile]

        repo_title_index = filePath.find("repos")
        if repo_title_index != -1:
            plot_title = filePath[repo_title_index:]
        else:
            plot_title = filePath

        # Generating a colormap
        colors = plt.cm.viridis(np.linspace(0, 1, len(x_ranges)))

        # Plotting the diagram with horizontal lines for ranges
        plt.figure(figsize=(10, 6))
        for i, (x_range, y_value, file_path) in enumerate(zip(x_ranges, y_values, file_names)):
            plt.hlines(y=y_value, xmin=x_range[0], xmax=x_range[1], color=colors[i], linewidth=2)
            plt.annotate(file_path, xy=(x_range[0], y_value), xytext=(5, 2), textcoords='offset points', fontsize=8, color=colors[i])

        plt.xlabel('Range')
        plt.ylabel('Value')
        plt.title(f'{plot_title}')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
