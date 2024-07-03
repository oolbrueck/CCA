from Simulator import Simulator
from JaccardSnippetGenerator import JaccardSnippetGenerator


class CodeCompletion:

    def __init__(self, pathToRepo):
        self.pathToRepo = pathToRepo

    def complete(self, file, cursorPosition):
        simulator = Simulator(self.pathToRepo)
        neighboringFiles = simulator.getNeighboringFiles(file)
        snippetGenerator = JaccardSnippetGenerator(neighboringFiles, 20, 60, file, cursorPosition)
        values = snippetGenerator.getSnippets()



