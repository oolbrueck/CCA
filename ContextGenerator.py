import tiktoken
import warnings

from Protocol import protocol_obj


# Die Aufgabe der Klasse besteht darin, die gesammelten Kontext-Fenster zu sortieren, als natürlich erscheinende Kommentare
# in den Kontext-String einzubetten und den Kontext zu reduzieren, falls die Anzahl der Tokens die Größe des Kontext-Fensters
# überschreitet.
class ContextGenerator:

    def __init__(self, windows, path, cursor_position, context_token_limit):
        self.path = path
        self.windows = windows
        self.cursor_position = cursor_position
        self.encoding_name = "cl100k_base"
        self.context_token_limit = context_token_limit

    def generate_context(self):
        self.__align_snippets()

        context_from_other_files = ""
        context_of_current_file = self.__get_context_from_current_file()
        protocol_obj.context_of_current_file = context_of_current_file
        for window in self.windows:
            context_from_other_files += self.__to_comment(window) + "\n\n"

        return self.reduce_context_if_necessary(context_from_other_files, context_of_current_file)

    # Code-Ausschnitte mit einem hohen übereinstimmungswert sollen dem Cursor am nächsten stehen
    def __align_snippets(self):
        self.windows.sort(key=lambda x: x['value'], reverse=True)

    # Funktion, die die Code-Ausschnitte als Kommentare präpariert
    def __to_comment(self, window):
        language_specific_comment = "//"
        first_line = language_specific_comment + "compare this snippet from " + window['file_path'] + ":\n"
        code = window['code'].split("\n")
        code = [language_specific_comment + line for line in code]
        code = first_line + "\n".join(code)
        return code

    # Funktion, die den Kontext des aktuellen Files zurückgibt und an der Stelle des Cursors "<insert Code here>" einfügt
    def __get_context_from_current_file(self):
        with open(self.path, 'r') as f:
            code = f.read()
        lines = code.split("\n")
        lines[self.cursor_position - 1] += "<insert Code here>"
        lines = [line for line in lines if line.strip()]
        context = "\n".join(lines)
        return context

    # Funktion, die den Kontext reduziert, sofern der gesammelte Kontext die größe des Kontext-Fensters überschreitet
    # Der Kontext wird um 10 Zeilen reduziert, bis die Anzahl der Tokens des Kontexts unter dem Limit liegt.
    def reduce_context_if_necessary(self, context_from_other_files, context_of_current_file): #todo protokol
        tokens_of_current_file = self.num_tokens_from_string(context_of_current_file)
        tokens_of_other_files = self.num_tokens_from_string(context_from_other_files)
        protocol_obj.num_tokens_of_current_file = tokens_of_current_file
        protocol_obj.num_tokens_of_other_files = tokens_of_other_files
        if tokens_of_current_file > self.context_token_limit:
            warnings.warn("Das aktuelle File enthält zu viele Tokens")
            protocol_obj.is_valid = False
        protocol_obj.removed_lines_from_context = ''
        if tokens_of_other_files + tokens_of_current_file > self.context_token_limit:
            while tokens_of_other_files + tokens_of_current_file > self.context_token_limit:
                removed_lines_from_context = context_from_other_files[-10:] #context_from_other_files.split("\n")[-10:] TODO was splitten wir hier ?
                protocol_obj.removedLinesFromContext = removed_lines_from_context + "\n" + protocol_obj.removed_lines_from_context
                context_from_other_files = context_from_other_files[:-10]
                tokens_of_other_files = self.num_tokens_from_string(context_from_other_files)

        return context_from_other_files + "\n" + context_of_current_file

    # Funktion, die die Anzahl der Tokens von einem Code-Bereich zurückgibt
    def num_tokens_from_string(self, code):
        encoding = tiktoken.get_encoding(self.encoding_name)
        num_tokens = len(encoding.encode(code))
        return num_tokens
