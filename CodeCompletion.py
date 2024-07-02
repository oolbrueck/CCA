from Simulator import Simulator
from SnippetGenerator import SnippetGenerator


class CodeCompletion:

    def __init__(self, pathToRepo):
        self.pathToRepo = pathToRepo

    def complete(self, file, cursorPosition):
        simulator = Simulator(self.pathToRepo)
        neighboringFiles = simulator.getNeighboringFiles(file)
        snippetGenerator = SnippetGenerator(neighboringFiles, 20, 60, file, cursorPosition)
        values = snippetGenerator.withJaccard()

        values.sort()
        print(values)


