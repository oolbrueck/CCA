import json  # Use the built-in json module
import matplotlib.pyplot as plt

allowedTopics = [
    "Array",
    "String",
    "Hash Table",
    "Dynamic Programming",
    "Math",
    "Sorting",
    "Greedy",
    "Depth-First Search",
    "Binary Search",
    "Tree",
    "Matrix",
    "Breadth-First Search",
    "Bit Manipulation",
    "Two Pointers",
    "Binary Tree",
    "Heap (Priority Queue)",
    "Prefix Sum",
    "Stack",
    "Simulation",
    "Graph",
    "Counting",
    "Sliding Window",
    "Backtracking",
    "Enumeration"
]
#
# # Function to filter JSON file
# def filterJsonFile():
#     with open('problemSets/leetCodeProblems.json') as f:
#         data = json.load(f)
#         filtered_data = [problem for problem in data if all(topic in allowedTopics for topic in problem['topics'])]
#         print(len(filtered_data))
#     with open('problemSets/leetCodeProblems.json', 'w') as f:
#         json.dump(filtered_data, f, indent=4)
#
# # Filter the JSON file first
# filterJsonFile()

# Now count the topics
with open("problemSets/leetCodeProblems.json") as g:
    data = json.load(g)

    #init an array called easy with len(allowedTopics) times zero
    easy = [0] * len(allowedTopics)
    medium = [0] * len(allowedTopics)
    hard = [0] * len(allowedTopics)

    for problem in data:
        for topic in problem["topics"]:
            if topic in allowedTopics:
                if problem["difficulty"] == "Easy":
                    easy[allowedTopics.index(topic)] += 1
                elif problem["difficulty"] == "Medium":
                    medium[allowedTopics.index(topic)] += 1
                else:
                    hard[allowedTopics.index(topic)] += 1

    print(easy)
    print(medium)
    print(hard)



# Create a bar chart to visualize the topic counts
plt.figure(figsize=(12, 8))  # Increase figure size to accommodate long x-axis labels
plt.bar(allowedTopics, easy, label='Easy', color='blue')
plt.bar(allowedTopics, medium, label='Medium', color='orange', bottom=easy)
plt.bar(allowedTopics, hard, label='Hard', color='red', bottom=[easy[i] + medium[i] for i in range(len(allowedTopics))])
plt.xlabel('Topics')
plt.ylabel('Counts')
#make a horizontal red line at y=20
plt.axhline(y=20, color='r', linestyle='--', label='20')
plt.title('Topic Counts in LeetCode Problems')
plt.xticks(rotation=90)  # Rotate x-axis labels
plt.tight_layout()  # Adjust layout to make room for x-axis labels
plt.show()


##############################################################


# pathToDir = "C:\Users\oligo\OneDrive\Bachelor Arbeit\Thesis\leetCode\Erste 100"
#pathToDir contains json files that have one object. The object hat the property url, get the last part of the url without any slashes
# and rename the file to that name
# import os
# import json
# import re
#
# def renameFiles(pathToDir):
#     for filename in os.listdir(pathToDir):
#         with open(f"{pathToDir}/{filename}") as f:
#             data = json.load(f)
#             url = data["url"]
#             name = re.search(r'/([^/]+)$', url).group(1)
#             os.rename(f"{pathToDir}/{filename}", f"{pathToDir}/{name}.json")
#
# renameFiles(pathToDir)
