from ContextGenerator import ContextGenerator
from OpenAIClient import OpenAIClient
from Simulator import Simulator
from SnippetGenerator import SnippetGenerator


class CodeCompletion:

    def __init__(self, pathToRepo):
        self.pathToRepo = pathToRepo

    def complete(self, file, cursorPosition):
        simulator = Simulator(self.pathToRepo)
        neighboringFiles = simulator.getNeighboringFiles(file)
        snippetGenerator = SnippetGenerator(neighboringFiles, 20, 60, file, cursorPosition, 'jaccard')
        snippets = snippetGenerator.getSnippets()
        contextGenerator = ContextGenerator(snippets, file, cursorPosition, 3000)
        context = contextGenerator.generateContext()
        openAIClient = OpenAIClient(context)
        response = openAIClient.submitPrompt()
        print("----------------------------------------------------")
        print("Response: ")
        print(response)


