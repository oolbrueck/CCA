
import re
import matplotlib.pyplot as plt

class SnippetGenerator:


    def __init__(self, neighboringFiles, domainWindowSize, coDomainWindowSize, currentFile, cursorPosition):
        self.neighboringFiles = neighboringFiles
        self.domainWindowSize = domainWindowSize
        self.coDomainWindowSize = coDomainWindowSize
        self.currentFile = currentFile
        self.cursorPosition = cursorPosition


    def withJaccard(self):
        domainWindowTokenized = self.__tokenizeCode(self.__getCodeFromDomainWindow())

        unionOfAllLists = (self.neighboringFiles['fileRelatedToParentClass'] +
                           self.neighboringFiles['filesRelatedToSiblingsClasses'] +
                           self.neighboringFiles['fileRelatedToImportedClasses'] +
                           self.neighboringFiles['fileRelatedToClassesFromNeighboringFiles'])

        jaccardValues = []

        for filePath in unionOfAllLists:
            slidingWindows = self.__getSlidingWindows(filePath)
            windowsOfSpecificFile = []

            for slidingWindow in slidingWindows:
                slidingWindowTokenized = self.__tokenizeCode(slidingWindow.get('code'))
                intersection = len(set(domainWindowTokenized).intersection(slidingWindowTokenized))
                union = len(set(domainWindowTokenized).union(slidingWindowTokenized))
                jaccardValue = intersection / union

                window = {}
                window['filePath'] = filePath
                window['fileCategory'] = self.__getFileCategory(filePath)
                window['range'] = slidingWindow.get('range')
                window['jaccardValue'] = jaccardValue
                window['code'] = slidingWindow

                windowsOfSpecificFile.append(window)

            # filteredWindowsOfSpecificFile = self.__filterWindowsOfSpecificFile(windowsOfSpecificFile)

            # Extracting ranges and jaccard values
            x_ranges = [window['range'] for window in windowsOfSpecificFile]
            y_jaccard_values = [window['jaccardValue'] for window in windowsOfSpecificFile]

            repo_title_index = filePath.find("repos")
            if repo_title_index != -1:
                plot_title = filePath[repo_title_index:]
            else:
                plot_title = filePath

            # Plotting the diagram with horizontal lines for ranges
            plt.figure(figsize=(10, 6))
            plt.hlines(y=y_jaccard_values, xmin=[r[0] for r in x_ranges], xmax=[r[1] for r in x_ranges], color='b', linewidth=2)
            plt.xlabel('Range')
            plt.ylabel('Jaccard Value')
            plt.title(f'{plot_title}')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

            jaccardValues.extend([(filePath, window['range'], window['jaccardValue']) for window in windowsOfSpecificFile])

        return jaccardValues



    def withCosine(self, file):
            return "snippet"

    def withLevenshtein(self, file):
        return "snippet"

    def __tokenizeCode(self, code):
        # Regex zum Trennen von Tokens basierend auf Leerzeichen und speziellen Zeichen
        tokens = re.findall(r"[\w']+|[(){}[\],.;]", code)
        return tokens


    def __getCodeFromDomainWindow(self):
        with open(self.currentFile, 'r') as f:
            code = f.read()
        lines = code.split("\n")
        line = lines[self.cursorPosition]
        domainWindow = ''.join(lines[int(self.cursorPosition - self.domainWindowSize * 0.5) : int(self.cursorPosition + self.domainWindowSize * 0.5)])

        return domainWindow

    def __getSlidingWindows(self, filePath):
        with open(filePath, 'r') as f:
            code = f.read()
        lines = code.split("\n")
        slidingWindows = []
        for i in range(0, len(lines) - self.coDomainWindowSize):
            window = {}
            window['code'] = ''.join(lines[i:i + self.coDomainWindowSize])
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

    def __filterWindowsOfSpecificFile(self, windowsOfSpecificFile):
        #filter windows with jaccard value > 0.5
        relevantWindows = [window for window in windowsOfSpecificFile if window['jaccardValue'] > 0.5]
        #sort windows by jaccard value
        relevantWindows.sort(key=lambda x: x['jaccardValue'], reverse=True)
        filterdWindows = []
        #add window with the highest jaccard value
        if len(relevantWindows) > 0:
            filterdWindows.append(relevantWindows[0])
        #add the rest of the windows if their range overlaps less than 20% with the range of the windows already added







