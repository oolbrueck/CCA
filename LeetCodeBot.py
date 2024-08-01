import json

from pynput.mouse import Controller as MouseController, Button as MouseButton
from pynput.keyboard import Controller as KeyboardController, Key
import time
import pyperclip



class LeetCodeBot:

    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def goToPage(self, page):
        with self.keyboard.pressed(Key.cmd):
            self.keyboard.press('m')
            self.keyboard.release('m')

        time.sleep(1)

        self.mouse.position = (2600, 1100)
        time.sleep(1)

        self.mouse.click(MouseButton.left)
        time.sleep(1)

        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('t')
            self.keyboard.release('t')

        time.sleep(1)

        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('l')
            self.keyboard.release('l')

        time.sleep(1)

        self.keyboard.type(page)

        time.sleep(1)

        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

        time.sleep(1)

    def getDifficulty(self):
        self.mouse.position = (1970, 280)
        time.sleep(1)
        self.mouse.click(MouseButton.left, 2)
        time.sleep(1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')
        time.sleep(1)
        difficulty = pyperclip.paste()
        time.sleep(1)
        print(difficulty)
        pyperclip.copy("ungültig")
        zwischenablage_inhalt = pyperclip.paste()
        time.sleep(1)
        return difficulty

    def closeTab(self):
        time.sleep(1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('w')
            self.keyboard.release('w')
        time.sleep(1)

    def openBrowserConsole(self):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press(Key.shift)
            self.keyboard.press('j')
            self.keyboard.release('j')
            self.keyboard.release(Key.shift)
        time.sleep(1)
        self.mouse.position = (3800, 350)
        time.sleep(1)

    def getContentFromConsole(self):
        jsTxt = '''
                    function extractTagValues() {
    var divElement1 = document.querySelector('div.mt-2.flex.flex-wrap.gap-1.pl-7');

    // Überprüfen, ob das Element existiert
    if (divElement1) {
        // Finde alle <a> Tags innerhalb des <div> Elements
        var anchorTags = divElement1.querySelectorAll('a');
        
        // Erstelle ein Array, um die Textinhalte der <a> Tags zu speichern
        var tagValues = [];
        
        // Iteriere über alle <a> Tags und sammle deren Textinhalte
        anchorTags.forEach(function(anchor) {
            tagValues.push(anchor.textContent);
        });
        return tagValues;
    } else {
        console.log("Element nicht gefunden");
    }
}

function convertHTMLContent(element) {
    // Hilfsfunktion, um <sup> Tags zu konvertieren
    function convertSuperscripts(node) {
        if (node.nodeType === Node.ELEMENT_NODE && node.tagName.toLowerCase() === 'sup') {
            return '^' + node.textContent;
        } else if (node.nodeType === Node.TEXT_NODE) {
            return node.textContent;
        }

        let result = '';
        node.childNodes.forEach(child => {
            result += convertSuperscripts(child);
        });

        return result;
    }

    return convertSuperscripts(element);
}


var divElement = document.querySelector('div.elfjS[data-track-load="description_content"]');

var txt = convertHTMLContent(divElement);
var topics = extractTagValues();
var resultString = txt
    .split('\\n')              
    .filter(line => line.trim() !== '')
    .join('\\n');             
console.log("$" + "$$" + resultString + "$" + "$$" + topics + "$" + "$$");
        '''
        pyperclip.copy(jsTxt)
        time.sleep(1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('v')
            self.keyboard.release('v')
        time.sleep(1)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

        time.sleep(1)
        self.mouse.click(MouseButton.left)
        time.sleep(1)

        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('a')
            self.keyboard.release('a')

        time.sleep(1)

        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')

        time.sleep(1)

        resultUnsplitted = pyperclip.paste()
        result = resultUnsplitted.split("$$$")

        return result[-3], result[-2]

    def closeBrowserConsole(self):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press(Key.shift)
            self.keyboard.press('j')
            self.keyboard.release('j')
            self.keyboard.release(Key.shift)
        time.sleep(1)

    def getCode(self):
        self.openCodeWindow()
        self.mouse.position = (1970, 220) #open menu
        time.sleep(1)
        self.mouse.click(MouseButton.left)
        time.sleep(1)
        self.mouse.position = (1970, 350) # go to python
        time.sleep(1)
        self.mouse.click(MouseButton.left)
        time.sleep(1)
        self.mouse.position = (2000, 350) #go to copy-position
        time.sleep(1)
        self.mouse.click(MouseButton.left, 4)
        time.sleep(1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')
        time.sleep(1)
        pyCode = pyperclip.paste()
        time.sleep(1)
        self.mouse.position = (1970, 220) #open menu
        time.sleep(1)
        self.mouse.click(MouseButton.left)
        time.sleep(1)
        self.mouse.position = (1970, 450) #select js
        time.sleep(1)
        self.mouse.click(MouseButton.left)
        time.sleep(1)
        self.mouse.position = (2000, 350) #go to copy-position
        time.sleep(1)
        self.mouse.click(MouseButton.left, 4)
        time.sleep(1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')
        time.sleep(1)
        jsCode = pyperclip.paste()
        time.sleep(1)
        self.mouse.position = (1970, 220) #open menu
        time.sleep(1)
        self.mouse.click(MouseButton.left)
        time.sleep(1)
        self.mouse.position = (1970, 300) #select js
        time.sleep(1)
        self.mouse.click(MouseButton.left)
        time.sleep(1)
        self.mouse.position = (2000, 350) #go to copy-position
        time.sleep(1)
        self.mouse.click(MouseButton.left, 4)
        time.sleep(1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')
        time.sleep(1)
        javaCode = pyperclip.paste()

        return pyCode, jsCode, javaCode

    def openCodeWindow(self):
        self.openBrowserConsole()
        time.sleep(1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('l')
            self.keyboard.release('l')
        time.sleep(1)
        code = '''
                var container = document.querySelector('div[data-layout-path="/c1/ts0"]');
                var button = container.querySelector('button.maximize');
                button.click();
                '''
        self.keyboard.type(code)
        time.sleep(1)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(1)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('l')
            self.keyboard.release('l')
        time.sleep(1)
        self.closeBrowserConsole()
        time.sleep(1)

    def getProblem(self, url):
        bot.goToPage(url)
        difficulty = bot.getDifficulty()
        bot.openBrowserConsole()
        excercise, topics = bot.getContentFromConsole()
        bot.closeBrowserConsole()
        givenPythonCode, givenJsCode, givenJavaCode = bot.getCode()
        bot.closeTab()

        # Sicherstellen, dass topics korrekt verarbeitet wird
        if topics:
            topics = topics.split(",")  # Split by comma
            topics = [topic.strip() for topic in topics]  # Remove leading/trailing whitespace
            topics = [topic.replace("'", "") for topic in topics]  # Optional: Remove single quotes if necessary
        else:
            topics = []

        #create a json object with the given data
        problem = {
            "excercise": excercise,
            "topics": topics,
            "url": url,
            "difficulty": difficulty,
            "givenPythonCode": givenPythonCode,
            "givenJsCode": givenJsCode,
            "givenJavaCode": givenJavaCode
        }

        #convert the object to json
        problem = json.dumps(problem)
        return problem



######################################################################

# with open("problemSets/leetCodeProblems.json") as g:
#     data = json.load(g)
#     bot = LeetCodeBot()
#     for problem in data:
#         #if problem has not the prop difficulty
#         if not problem.get('difficulty'):
#             bot.goToPage(problem.get('url'))
#             difficulty = bot.getDifficulty()
#             problem['difficulty'] = difficulty
#             bot.closeTab()
#
#     with open('problemSets/leetCodeProblems.json', 'w') as f:
#         json.dump(data, f, indent=4)

bot = LeetCodeBot()


problems = ["https://leetcode.com/problems/invert-binary-tree/description/",
            "https://leetcode.com/problems/binary-tree-paths/",
            "https://leetcode.com/problems/island-perimeter/",
            "https://leetcode.com/problems/minimum-absolute-difference-in-bst/",
            "https://leetcode.com/problems/binary-tree-tilt/",
            "https://leetcode.com/problems/minimum-height-trees/",
            "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
            "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/",
            "https://leetcode.com/problems/kth-smallest-element-in-a-bst/",
            "https://leetcode.com/problems/course-schedule-ii/",
            "https://leetcode.com/problems/number-of-islands/",
            "https://leetcode.com/problems/binary-tree-right-side-view/",
            "https://leetcode.com/problems/cheapest-flights-within-k-stops/",
            "https://leetcode.com/problems/all-paths-from-source-to-target/",
            "https://leetcode.com/problems/find-eventual-safe-states/",
            "https://leetcode.com/problems/making-a-large-island/",
            "https://leetcode.com/problems/sum-of-distances-in-tree/",
            "https://leetcode.com/problems/similar-string-groups/",
            "https://leetcode.com/problems/minimize-malware-spread/",
            "https://leetcode.com/problems/minimize-malware-spread-ii/"]


for problem in problems:
    problemAsJSON = bot.getProblem(problem)
    #The File leetCodeProblems.json contains an array of objects. Add problemAsJSON to the array
    with open("problemSets/leetCodeProblems.json") as f:
        data = json.load(f)
        data.append(json.loads(problemAsJSON))
    #Write the modified array back to the file
    with open('problemSets/leetCodeProblems.json', 'w') as f:
        json.dump(data, f, indent=4)
    time.sleep(2)






