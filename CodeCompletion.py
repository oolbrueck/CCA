from ContextGenerator import ContextGenerator
from OpenAIClient import OpenAIClient
from Simulator import Simulator
from JaccardSnippetGenerator import JaccardSnippetGenerator


class CodeCompletion:

    def __init__(self, pathToRepo):
        self.pathToRepo = pathToRepo

    def complete(self, file, cursorPosition):
        simulator = Simulator(self.pathToRepo)
        neighboringFiles = simulator.getNeighboringFiles(file)
        snippetGenerator = JaccardSnippetGenerator(neighboringFiles, 20, 60, file, cursorPosition)
        snippets = snippetGenerator.getSnippets()
        contextGenerator = ContextGenerator(snippets, file, cursorPosition, 3000)
        context = contextGenerator.generateContext()
        openAIClient = OpenAIClient(context)
        response = openAIClient.submitPrompt()

        print("Response: ")
        print(response)


