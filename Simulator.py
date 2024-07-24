import os

import javalang
import warnings

from Protocol import protocol_obj


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

    def __init__(self, path_to_repo):
        self.path_to_repo = path_to_repo
        self.classes_with_their_path, self.classes_with_their_parent = self.__get_class_structure()

    # Die Funktion gibt zwei Dictionaries zurück, welche zum einen die Klassen und deren Pfade und zum anderen
    # die Klassen und deren Elternklasse enthalten, welche im Repository vorhanden sind.
    # In dieser Funktion wird dazu das gesamte Repository durchsucht.
    def __get_class_structure(self):
        classes_with_paths = {}
        classes_with_parent_class = {}

        if os.path.exists(
                "project_structure.json"):  # Da das traversieren des Repositories dauern kann, wird die Struktur beim ersten Durchlauf in einer Datei gespeichert
            import json
            with open("project_structure.json", "r") as f:
                data = json.load(f)
                return data["classesWithPaths"], data["classesWithParentClass"]
        else:
            for root, dirs, files in os.walk(self.path_to_repo):
                for file in files:
                    if file.endswith(".java"):
                        file_path = os.path.join(root, file)

                        class_name = self.__get_class_name_from_file(file_path)

                        if class_name is not None:
                            classes_with_paths[class_name] = file_path

                            with open(file_path, 'r') as f:
                                java_code = f.read()

                            tree = javalang.parse.parse(java_code)

                            for _, node in tree.filter(javalang.tree.ClassDeclaration):
                                if node.name == class_name:
                                    parent_class = node.extends.name if node.extends else None
                                    if parent_class:
                                        classes_with_parent_class[class_name] = parent_class
            for key in classes_with_paths.keys():
                classes_with_paths[key] = classes_with_paths[key].replace("\\", "/")

            import json
            with open("project_structure.json", "w") as f:
                json.dump({"classesWithPaths": classes_with_paths, "classesWithParentClass": classes_with_parent_class},
                          f)

        return classes_with_paths, classes_with_parent_class

    # Die Funktion gibt die "benachbarten Files" des übergebenen Files zurück.
    def get_neighboring_files(self, file):
        neighboring_files = {}
        class_of_file = self.__get_class_name_from_file(file)

        parent_class = self.__get_parent_class(file)
        siblings_classes = self.__get_child_classes(parent_class)
        imported_classes = self.__get_imported_classes(file)
        classes_from_neighboring_files = self.__get_classes_from_neighboring_files(file)

        temp = [parent_class, siblings_classes, imported_classes, classes_from_neighboring_files]

        file_counter = 0
        already_added_files = []

        for i in range(len(temp)):
            # Wir holen uns die Liste von temp[i] durch Index-Zugriff
            current_list = temp[i]
            j = 0
            while j < len(current_list) and file_counter < 20:
                cls = current_list[j]
                if cls in already_added_files or cls == class_of_file:
                    # Entferne das Element, wenn es bereits hinzugefügt wurde
                    current_list.pop(j)  # Pop entfernt das Element und verschiebt den Rest nach vorne
                else:
                    # Füge das Element der Liste der bereits hinzugefügten Dateien hinzu
                    already_added_files.append(cls)
                    file_counter += 1
                    j += 1  # Erhöhe den Index nur, wenn wir ein neues Element hinzufügen

        if file_counter < 20:
            warnings.warn("Es konnten nicht genügend Dateien gefunden werden, um den Kontext zu simulieren.")
            # setzte im Protokol das attribut valid auf false
            protocol_obj.is_valid = False

        #for each array in temp and each class-string in the array, replace the class-string with the path to the class
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                temp[i][j] = self.get_path_to_class(temp[i][j])

        neighboring_files['file_related_to_parent_class'] = temp[0]
        neighboring_files['files_related_to_siblings_classes'] = temp[1]
        neighboring_files['file_related_to_imported_classes'] = temp[2]
        neighboring_files['file_related_to_classes_from_neighboring_files'] = temp[3]

        protocol_obj.neighboring_files = neighboring_files
        return neighboring_files



        # print("number of elements of classes_from_neighboring_files " + str(len(classes_from_neighboring_files)))
        #
        # neighboring_files['file_related_to_parent_class'] = [self.get_path_to_class(parent_class)]
        #
        # # Dient dazu, dass keine doppelten Files in den Kontext einbezogen werden
        # unique_files = dict.fromkeys(neighboring_files['file_related_to_parent_class'])
        #
        # neighboring_files['files_related_to_siblings_classes'] = []
        # for cls in siblings_classes:
        #     path = self.get_path_to_class(cls)
        #     if path not in unique_files:
        #         neighboring_files['files_related_to_siblings_classes'].append(path)
        #         unique_files.add(path)
        #
        # neighboring_files['file_related_to_imported_classes'] = []
        # for cls in imported_classes:
        #     path = self.get_path_to_class(cls)
        #     if path not in unique_files:
        #         neighboring_files['file_related_to_imported_classes'].append(path)
        #         unique_files.add(path)
        #
        # neighboring_files['file_related_to_classes_from_neighboring_files'] = []
        # for cls in classes_from_neighboring_files:
        #     path = self.get_path_to_class(cls)
        #     if path not in unique_files:
        #         neighboring_files['file_related_to_classes_from_neighboring_files'].append(path)
        #         unique_files.add(path)
        #
        # union_of_all_files = (
        #             neighboring_files['file_related_to_parent_class'] + neighboring_files['files_related_to_siblings_classes']
        #             + neighboring_files['file_related_to_imported_classes'] + neighboring_files[
        #                 'file_related_to_classes_from_neighboring_files'])
        #
        # print("union_of_all_files: " + str(union_of_all_files))
        #
        # print("number of elements of union_of_all_files " + str(len(union_of_all_files)))
        # if len(unique_files) < 20:
        #     warnings.warn("Es konnten nicht genügend Dateien gefunden werden, um den Kontext zu simulieren.")
        #     # setzte im Protokol das attribut valid auf false
        #     protocol_obj.is_valid = False
        #
        # files_to_exclude = []  # Liste der Files, die nicht in den Kontext einbezogen werden sollen, da die Gesamtanzahl der Files > 20 ist
        # if len(union_of_all_files) > 20:
        #     files_to_exclude = union_of_all_files[20:]
        #
        # for key in neighboring_files.keys():  # Die identifizierten Files werden aus dem neighboring_files-Dictionary entfernt
        #     neighboring_files[key] = [path for path in neighboring_files[key] if path not in files_to_exclude]
        #
        # protocol_obj.neighboring_files = neighboring_files
        # return neighboring_files

    def __get_class_name_from_file(self, file_path):
        with open(file_path, 'r') as file:
            java_code = file.read()

        try:
            tree = javalang.parse.parse(java_code)
            for path, node in tree:
                if isinstance(node, javalang.tree.ClassDeclaration):
                    return node.name
        except javalang.parser.JavaSyntaxError as e:
            print(f"Syntaxfehler beim Parsen der Datei {file_path}: {e}")
            return None
        except Exception as e:
            print(f"Fehler beim Analysieren der Datei {file_path}: {e}")
            return None

    def __get_parent_class(self, file_path):
        parent = None
        for key, value in self.classes_with_their_path.items():
            if value == file_path:
                parent = key
                break
        return [parent] if parent is not None else []

    def __get_child_classes(self, parentClass):
        children = []
        for key, value in self.classes_with_their_parent.items():
            if value == parentClass:
                children.append(key)
        return children

    def __get_imported_classes(self, file_path):
        imported_classes = []
        with open(file_path, 'r') as file:
            java_code = file.read()
        try:
            tree = javalang.parse.parse(java_code)
            for path, node in tree:
                if isinstance(node, javalang.tree.Import):
                    imported_classes.append(node.path)
        except javalang.parser.JavaSyntaxError as e:
            print(f"Syntaxfehler beim Parsen der Datei {file_path}: {e}")
        except Exception as e:
            print(f"Fehler beim Analysieren der Datei {file_path}: {e}")

        imported_classes_that_belong_to_repo = []
        for imported_class in imported_classes:
            for key in self.classes_with_their_path.keys():
                if imported_class.endswith(key):
                    class_name = imported_class.split('.')[-1]
                    imported_classes_that_belong_to_repo.append(class_name)
        return imported_classes_that_belong_to_repo

    def __get_classes_from_neighboring_files(self, file_path):
        neighboring_classes = []

        for key, value in self.classes_with_their_path.items():
            #print(os.path.dirname(value) + " == " + os.path.dirname(file_path) + " and " + value + " != " + file_path)
            if os.path.dirname(value) == os.path.dirname(file_path) and value != file_path:
                neighboring_classes.append(key)
        return neighboring_classes

    def get_path_to_class(self, class_name):
        return self.classes_with_their_path.get(class_name, None)
