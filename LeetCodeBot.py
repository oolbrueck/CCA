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

problems = ['https://leetcode.com/problems/3sum-closest/', 'https://leetcode.com/problems/coin-change/',
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






