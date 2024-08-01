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


# there is a file problemSets/leetCodeProblems.json which contains an array of objects
# iterate over all objects in the array which is in the json-file
# count the objects where difficulty is not in ["Easy", "Medium", "Hard"] and print the count on the console
# import json
#
# with open('problemSets/leetCodeProblems.json') as f:
#     data = json.load(f)
#     urls = []
#     count = 0
#     for problem in data:
#         if problem['difficulty'] not in ['Easy', 'Medium', 'Hard']:
#             urls.append(problem['url'])
#
#     print(urls)
#

urlsFromProblemsThatShallBeRemoved = ['https://leetcode.com/problems/3sum-closest/', 'https://leetcode.com/problems/coin-change/',
            'https://leetcode.com/problems/continuous-subarray-sum/', 'https://leetcode.com/problems/decode-ways/',
            'https://leetcode.com/problems/optimal-division/', 'https://leetcode.com/problems/palindrome-partitioning/',
            'https://leetcode.com/problems/reconstruct-original-digits-from-english/',
            'https://leetcode.com/problems/find-eventual-safe-states/',
            'https://leetcode.com/problems/recover-a-tree-from-preorder-traversal/description/',
            'https://leetcode.com/problems/create-binary-tree-from-descriptions/description/',
            'https://leetcode.com/problems/root-equals-sum-of-children/description/',
            'https://leetcode.com/problems/spiral-matrix/description/',
            'https://leetcode.com/problems/toeplitz-matrix/description/',
            'https://leetcode.com/problems/special-positions-in-a-binary-matrix/description/',
            'https://leetcode.com/problems/number-of-increasing-paths-in-a-grid/description/',
            'https://leetcode.com/problems/strange-printer-ii/description/',
            'https://leetcode.com/problems/cycle-length-queries-in-a-tree/description/',
            'https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/description/',
            'https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/description/',
            'https://leetcode.com/problems/minimum-number-of-operations-to-sort-a-binary-tree-by-level/description/',
            'https://leetcode.com/problems/make-array-zero-by-subtracting-equal-amounts/description/',
            'https://leetcode.com/problems/last-stone-weight/description/',
            'https://leetcode.com/problems/minimum-cost-to-hire-k-workers/description/',
            'https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/description/',
            'https://leetcode.com/problems/minimum-space-wasted-from-packaging/description/',
            'https://leetcode.com/problems/stamping-the-grid/description/',
            'https://leetcode.com/problems/longest-well-performing-interval/description/',
            'https://leetcode.com/problems/count-of-interesting-subarrays/description/',
            'https://leetcode.com/problems/ant-on-the-boundary/description/',
            'https://leetcode.com/problems/text-justification/description/',
            'https://leetcode.com/problems/find-winner-on-a-tic-tac-toe-game/description/',
            'https://leetcode.com/problems/add-binary/description/',
            'https://leetcode.com/problems/count-visited-nodes-in-a-directed-graph/description/',
            'https://leetcode.com/problems/cat-and-mouse/description/',
            'https://leetcode.com/problems/frog-position-after-t-seconds/description/',
            'https://leetcode.com/problems/most-profitable-path-in-a-tree/description/',
            'https://leetcode.com/problems/course-schedule-ii/description/',
            'https://leetcode.com/problems/flower-planting-with-no-adjacent/description/',
            'https://leetcode.com/problems/find-if-path-exists-in-graph/description/',
            'https://leetcode.com/problems/number-of-different-subsequences-gcds/description/',
            'https://leetcode.com/problems/replace-question-marks-in-string-to-minimize-its-value/description/',
            'https://leetcode.com/problems/minimum-length-of-anagram-concatenation/description/',
            'https://leetcode.com/problems/most-common-word/description/',
            'https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/description/',
            'https://leetcode.com/problems/take-k-of-each-character-from-left-and-right/description/',
            'https://leetcode.com/problems/maximum-average-subarray-i/description/',
            'https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/description/',
            'https://leetcode.com/problems/find-the-maximum-number-of-elements-in-subset/description/']

# there is a file problemSets/leetCodeProblems.json which contains an array of objects
# remove all objects where the url is in the list urlsFromProblemsThatShallBeRemoved





