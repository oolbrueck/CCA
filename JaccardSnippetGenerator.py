import re
import matplotlib.pyplot as plt
import numpy as np


class JaccardSnippetGenerator:

    def __init__(self, neighboringFiles, domainWindowSize, coDomainWindowSize, currentFile, cursorPosition):
        self.neighboringFiles = neighboringFiles
        self.domainWindowSize = domainWindowSize
        self.coDomainWindowSize = coDomainWindowSize
        self.currentFile = currentFile
        self.cursorPosition = cursorPosition

    def getSnippets(self):
        domainWindowTokenized = self.__tokenizeCode(self.__getCodeFromDomainWindow())

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

            filteredWindowsOfSpecificFile = self.__filterWindowsOfSpecificFile(windowsOfSpecificFile)

            filteredWindowsOfAllFiles.extend(filteredWindowsOfSpecificFile)

        for window in filteredWindowsOfAllFiles:
            print(f"filePath: {window['filePath']}, fileCategory: {window['fileCategory']}, range: {window['range']}, jaccardValue: {window['jaccardValue']}")

        self.__printPlot(filteredWindowsOfAllFiles, '')

        return filteredWindowsOfAllFiles

    # def withCosine(self, file):
    #         return "snippet"
    #
    # def withLevenshtein(self, file):
    #     return "snippet"

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
        line = lines[self.cursorPosition - 1] + "<insert Code here>"
        lines[self.cursorPosition - 1] = line
        lines = [line for line in lines if line.strip()]  # Remove empty lines
        #get the line that contains the substring "<insert Code here>"
        cursorPositionAfterRemovingEmptyLines = [i for i, line in enumerate(lines) if "<insert Code here>" in line][0]

        modified_lines = [line + "\n" for line in lines]
        domainWindow = "".join(modified_lines[cursorPositionAfterRemovingEmptyLines - int(self.domainWindowSize / 2):cursorPositionAfterRemovingEmptyLines + 1 + int(self.domainWindowSize / 2)])

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

    # Funktion dient dazu die Fenster herauszufiltern, welche einen Schwellenwert erfüllen und
    # gleichzeitig sich nicht zu stark überlappen
    def __filterWindowsOfSpecificFile(self, windowsOfSpecificFile):
        intersectionThreshold = 0.2
        jaccardValueThreshold = 0.2

        thresholdFulfillingWindows = [window for window in windowsOfSpecificFile if
                                      window['jaccardValue'] > jaccardValueThreshold]
        thresholdFulfillingWindows.sort(key=lambda x: x['jaccardValue'], reverse=True)

        for window in thresholdFulfillingWindows:  # Die beiden Zahlwerte in range werden zu einer Sequenz umgewandelt um später die Überschneidung zu berechnen
            window['range'] = list(range(window['range'][0], window['range'][1]))

        disjunctWindows = []  # inklusive disjunkte und fast disjunkte Windows (siehe intersectionThreshold)

        if len(thresholdFulfillingWindows) > 0:
            disjunctWindows.append(thresholdFulfillingWindows[
                                       0])  # Füge das erste Fenster hinzu, da es das Fenster mit dem höchsten Jaccard-Wert ist

        for window in thresholdFulfillingWindows[
                      1:]:  # Iteriere absteigend (bezogen auf den Jaccard-Wert) über alle Fenster und füge sie hinzu
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

    def __printPlot(self, windowsOfSpecificFile, filePath):
        print("plo")
        # Extracting ranges, jaccard values, and file paths
        x_ranges = [window['range'] for window in windowsOfSpecificFile]
        y_jaccard_values = [window['jaccardValue'] for window in windowsOfSpecificFile]
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
        for i, (x_range, y_value, file_path) in enumerate(zip(x_ranges, y_jaccard_values, file_names)):
            plt.hlines(y=y_value, xmin=x_range[0], xmax=x_range[1], color=colors[i], linewidth=2)
            plt.annotate(file_path, xy=(x_range[0], y_value), xytext=(5, 2), textcoords='offset points', fontsize=8, color=colors[i])

        plt.xlabel('Range')
        plt.ylabel('Jaccard Value')
        plt.title(f'{plot_title}')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
