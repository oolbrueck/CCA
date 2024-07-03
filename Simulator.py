import os

import javalang
from pydantic import warnings


# Die Klasse Simulator dient dazu der CodeCompletion-Klasse Files zur verfügung zu stellen, welche als Kontext angesehen werden können.
# Bei Code-Assitenten wie GitHub Copilot speist sich der Kontext aus dem aktuellen File sowie weiteren Files in geöffneten Tabs (max. 20).
# Dieses Nutzerverhalten kann durch die Klasse Simulator in ansätzen simuliert werden, indem sie die Klassen und Dateistruktur
# des aktuellen Files analysiert.
# Es werden zurückgegeben:
# - Die Elternklasse des aktuellen Files bzw. dessen File
# - Die Kindklassen der Elternklasse bzw. deren Files
# - Die importierten Klassen des aktuellen Files bzw. deren Files
# - Die Klassen der Files, die sich im selben Verzeichnis wie das aktuelle File befinden, bzw. deren Files
#
# Die Files werden kategorisiert bereitgestellt, um die Verwendung in der CodeCompletion-Klasse zu erleichtern.
class Simulator:

    def __init__(self, pathToRepo):
        self.pathToRepo = pathToRepo
        self.classesWithTheirPath, self.classesWithTheirParent = self.__getClassStructure(pathToRepo)

    # Die Funktion gibt zwei Dictionaries zurück, welche zum einen die Klassen und deren Pfade und zum anderen
    # die Klassen und deren Elternklasse enthalten, welche im Repository vorhanden sind.
    # In dieser Funktion wird dazu das gesamte Repository durchsucht.
    def __getClassStructure(self, pathToRepo):
        classesWithPaths = {}
        classesWithParentClass = {}

        if os.path.exists("project_structure.json"): # Da das traversieren des Repositories dauern kann, wird die Struktur beim ersten Durchlauf in einer Datei gespeichert
            import json
            with open("project_structure.json", "r") as f:
                data = json.load(f)
                return data["classesWithPaths"], data["classesWithParentClass"]
        else:
            for root, dirs, files in os.walk(pathToRepo):
                for file in files:
                    if file.endswith(".java"):
                        filepath = os.path.join(root, file)

                        className = self.__getClassNameFromFile(filepath)

                        if className is not None:
                            classesWithPaths[className] = filepath

                            with open(filepath, 'r') as f:
                                java_code = f.read()

                            tree = javalang.parse.parse(java_code)

                            for _, node in tree.filter(javalang.tree.ClassDeclaration):
                                if node.name == className:
                                    parent_class = node.extends.name if node.extends else None
                                    if parent_class:
                                        classesWithParentClass[className] = parent_class

            import json
            with open("project_structure.json", "w") as f:
                json.dump({"classesWithPaths": classesWithPaths, "classesWithParentClass": classesWithParentClass}, f)

        return classesWithPaths, classesWithParentClass


    # Die Funktion gibt die "benachbarten Files" des übergebenen Files zurück.
    def getNeighboringFiles(self, file):
        neighboringFiles = {}
        parentClass = ''
        siblingsClasses = []
        importedClasses = []
        classesFromNeighboringFiles = []

        parentClass = self.__getParentClass(file)
        siblingsClasses = self.__getChildClasses(parentClass)
        importedClasses = self.__getImportedClasses(file)
        classesFromNeighboringFiles = self.__getClassesFromNeighboringFiles(file)

        neighboringFiles['fileRelatedToParentClass'] = [self.getPathToClass(parentClass)]

        # dient dazu, dass keine doppelten Files in den Kontext einbezogen werden
        unique_files = set(neighboringFiles['fileRelatedToParentClass'])

        neighboringFiles['filesRelatedToSiblingsClasses'] = []
        for cls in siblingsClasses:
            path = self.getPathToClass(cls)
            if path not in unique_files:
                neighboringFiles['filesRelatedToSiblingsClasses'].append(path)
                unique_files.add(path)

        neighboringFiles['fileRelatedToImportedClasses'] = []
        for cls in importedClasses:
            path = self.getPathToClass(cls)
            if path not in unique_files:
                neighboringFiles['fileRelatedToImportedClasses'].append(path)
                unique_files.add(path)

        neighboringFiles['fileRelatedToClassesFromNeighboringFiles'] = []
        for cls in classesFromNeighboringFiles:
            path = self.getPathToClass(cls)
            if path not in unique_files:
                neighboringFiles['fileRelatedToClassesFromNeighboringFiles'].append(path)
                unique_files.add(path)


        unionOfAllLists = (neighboringFiles['fileRelatedToParentClass'] + neighboringFiles['filesRelatedToSiblingsClasses']
                           + neighboringFiles['fileRelatedToImportedClasses'] + neighboringFiles['fileRelatedToClassesFromNeighboringFiles'])

        if len(unionOfAllLists) < 20:
            warnings.warn("Es konnten nicht genügend Dateien gefunden werden, um den Kontext zu simulieren.")

        filesToExclude = [] # Liste der Files, die nicht in den Kontext einbezogen werden sollen, da die gesamtanzahl der Files > 20 ist
        if len(unionOfAllLists) > 20:
            filesToExclude = unionOfAllLists[20:]

        for key in neighboringFiles.keys(): # Die identifizierten Files werden aus dem neighboringFiles-Dictionary entfernt
            neighboringFiles[key] = [path for path in neighboringFiles[key] if path not in filesToExclude]

        return neighboringFiles

    def __getClassNameFromFile(self, filePath):
        with open(filePath, 'r') as file:
            javaCode = file.read()

        try:
            tree = javalang.parse.parse(javaCode)
            for path, node in tree:
                if isinstance(node, javalang.tree.ClassDeclaration):
                    return node.name
        except javalang.parser.JavaSyntaxError as e:
            print(f"Syntaxfehler beim Parsen der Datei {filePath}: {e}")
            return None
        except Exception as e:
            print(f"Fehler beim Analysieren der Datei {filePath}: {e}")
            return None

    def __getParentClass(self, filePath):
        parent = None
        for key, value in self.classesWithTheirPath.items():
            if value == filePath:
                parent = key
                break
        return self.classesWithTheirParent.get(parent, None)

    def __getChildClasses(self, parentClass):
        children = []
        for key, value in self.classesWithTheirParent.items():
            if value == parentClass:
                children.append(key)
        return children

    def __getImportedClasses(self, filePath):
        importedClasses = []
        with open(filePath, 'r') as file:
            javaCode = file.read()
        try:
            tree = javalang.parse.parse(javaCode)
            for path, node in tree:
                if isinstance(node, javalang.tree.Import):
                    importedClasses.append(node.path)
        except javalang.parser.JavaSyntaxError as e:
            print(f"Syntaxfehler beim Parsen der Datei {filePath}: {e}")
        except Exception as e:
            print(f"Fehler beim Analysieren der Datei {filePath}: {e}")

        importedClassesThatBelongToRepo = []
        for importedClass in importedClasses:
            for key in self.classesWithTheirPath.keys():
                if importedClass.endswith(key):
                    className = importedClass.split('.')[-1]
                    importedClassesThatBelongToRepo.append(className)
        return importedClassesThatBelongToRepo

    def __getClassesFromNeighboringFiles(self, filePath):
        neighboringClasses = []

        for key, value in self.classesWithTheirPath.items():
            if os.path.dirname(value) == os.path.dirname(filePath) and value != filePath:
                neighboringClasses.append(key)
        return neighboringClasses

    def getPathToClass(self, className):
        return self.classesWithTheirPath.get(className, None)


