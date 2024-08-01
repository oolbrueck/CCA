import os
import json
import re
#
# pathToDir = r"C:\Users\oligo\OneDrive\Bachelor Arbeit\Thesis\leetCode\Zweite 100"
#
# def renameFiles(pathToDir):
#     for filename in os.listdir(pathToDir):
#         file_path = os.path.join(pathToDir, filename)
#
#         # Überprüfen, ob es sich bei dem Eintrag um eine Datei handelt
#         if os.path.isfile(file_path):
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 try:
#                     data = json.load(f)
#                     url = data.get("url", "")
#                     # Angepasster regulärer Ausdruck, um das letzte Segment der URL zu erfassen
#                     match = re.search(r'/([^/]+)/?$', url)
#
#                     if match:
#                         name = match.group(1)
#                         new_file_path = os.path.join(pathToDir, f"{name}.json")
#                         # Datei schließen, bevor sie umbenannt wird
#                         f.close()
#                         os.rename(file_path, new_file_path)
#                         print(f"Renamed {file_path} to {new_file_path}")
#                     else:
#                         print(f"No match found for URL: {url}")
#                 except json.JSONDecodeError as e:
#                     print(f"Error decoding JSON in file {file_path}: {e}")
#                 except Exception as e:
#                     print(f"Error processing file {file_path}: {e}")
#
# renameFiles(pathToDir)



## put for each object in ./problemSets/leetCodeProblems.json its props givenPythonCode, givenJsCode and givenJavaCode in a set, that doesnt allow duplicates
## and print each object's url on the console where the set has less than 3 elements
# import json
# from collections import defaultdict
#
# # Read the JSON file
# with open('problemSets/leetCodeProblems.json') as f:
#     data = json.load(f)
#
#     # Create a dictionary to store the code snippets for each URL
#     code_snippets = defaultdict(set)
#
#     # Iterate over each problem in the data
#     for problem in data:
#         url = problem.get('url')
#         python_code = problem.get('givenPythonCode')
#         js_code = problem.get('givenJsCode')
#         java_code = problem.get('givenJavaCode')
#
#         # Add the code snippets to the set for the URL
#         if python_code:
#             code_snippets[url].add(python_code)
#         if js_code:
#             code_snippets[url].add(js_code)
#         if java_code:
#             code_snippets[url].add(java_code)
#
#     # Print the URLs with less than 3 unique code snippets
#     for url, snippets in code_snippets.items():
#         if len(snippets) < 3:
#             print(f"URL: {url} Number of unique code snippets: {len(snippets)}")
#             print(snippets)
#             print()
#
#             # if the set contains an element-String x which has the substring "(self,", set the prop givenPythonCode of the object to x
#             # if the set contains an element-String y which has the substring "function(", set the prop givenJsCode of the object to y
#             # if the set contains an element-String z which has the substring "public", set the prop givenJavaCode of the object to z
#
#             for snippet in snippets:
#                 if "(self," in snippet:
#                     for problem in data:
#                         if problem.get('url') == url:
#                             problem['givenPythonCode'] = snippet
#                             break
#                 if "function(" in snippet:
#                     for problem in data:
#                         if problem.get('url') == url:
#                             problem['givenJsCode'] = snippet
#                             break
#                 if "public" in snippet:
#                     for problem in data:
#                         if problem.get('url') == url:
#                             problem['givenJavaCode'] = snippet
#                             break
#
# # Write the modified data back to the JSON file
# with open('problemSets/leetCodeProblems.json', 'w') as f:
#     json.dump(data, f, indent=4)



##########################################################################################

#read all json-files that are in the directory ./problemSets/leetCodeProblems . A File contains only one object with the prop Topics (its an array).
#count how many objects have the topic "Matrix" in the array Topics and print the count on the console
import json
import os

# Define the directory containing the JSON files
directory = r"C:\Users\oligo\OneDrive\Bachelor Arbeit\Thesis\leetCode"

# Initialize the count of objects with the topic "Matrix"
matrix_count = 0

# Iterate over each file in the directory
for filename in os.listdir(directory):
    # Construct the full path to the file
    file_path = os.path.join(directory, filename)

    # Check if the entry is a file
    if os.path.isfile(file_path):
        # Open the file and load the JSON data
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Check if the 'Topics' key is present in the data
            if 'topics' in data:
                # Check if the 'Matrix' topic is present in the list of topics
                if 'Matrix' in data['topics']:
                    matrix_count += 1

# Print the count of objects with the topic "Matrix"
print(f"Number of objects with the topic 'Matrix': {matrix_count}")





