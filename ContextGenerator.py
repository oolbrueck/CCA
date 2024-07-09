import tiktoken
from pydantic import warnings


class ContextGenerator:

    def __init__(self, windows, path, cursorPosition, contextTokenLimit):
        self.path = path
        self.windows = windows
        self.cursorPosition = cursorPosition
        self.encoding_name = "cl100k_base"
        self.contextTokenLimit = contextTokenLimit


    def generateContext(self):
        self.__alignSnippets()

        contextFromOtherFiles = ""
        contextOfCurrentFile = self.__getContextFromCurrentFile()
        for window in self.windows:
            contextFromOtherFiles += self.__toComment(window) + "\n\n"

        return self.reduceContextIfNeccessary(contextFromOtherFiles, contextOfCurrentFile)


    def __alignSnippets(self):
        self.windows.sort(key=lambda x: x['value'], reverse=True)

    def __toComment(self, window):
        languageSpecificComment = "//"
        firstLine = languageSpecificComment + "compare this snippet from " + window['filePath'] + ":\n"
        #window['code'] is a multiline string, add languageSpecificComment to each line at the beginning
        code = window['code'].split("\n")
        code = [languageSpecificComment + line for line in code]
        #join all lines to a single string and add the firstLine to the beginning of the
        code = firstLine + "\n".join(code)
        return code

    #creates a multiline-String from the content in the file and adds the String <insert Code here> at the cursorPosition
    def __getContextFromCurrentFile(self):
        with open(self.path, 'r') as f:
            code = f.read()
        lines = code.split("\n")
        line = lines[self.cursorPosition - 1] + "<insert Code here>"
        lines[self.cursorPosition - 1] = line
        lines = [line for line in lines if line.strip()]
        #concatenate all lines to a single multiline-string
        context = "\n".join(lines)
        return context

    def reduceContextIfNeccessary(self, contextFromOtherFiles, contextOfCurrentFile):
        tokensOfCurrentFile = self.num_tokens_from_string(contextOfCurrentFile)
        tokensOfOtherFiles = self.num_tokens_from_string(contextFromOtherFiles)
        if(tokensOfCurrentFile > self.contextTokenLimit):
            warnings.warn("Das aktuelle File enthält zu viele Tokens")
        if(tokensOfOtherFiles + tokensOfCurrentFile > self.contextTokenLimit):
            #reduce 10 characters from contextOfOtherFiles until the limit is reached
            while(tokensOfOtherFiles + tokensOfCurrentFile > self.contextTokenLimit):
                contextFromOtherFiles = contextFromOtherFiles[:-10]
                tokensOfOtherFiles = self.num_tokens_from_string(contextFromOtherFiles)

        return contextFromOtherFiles + "\n" + contextOfCurrentFile



    def num_tokens_from_string(self, code):
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(self.encoding_name)
        num_tokens = len(encoding.encode(code))
        return num_tokens


