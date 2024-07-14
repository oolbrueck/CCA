import sys

from ContextGenerator import ContextGenerator
from OpenAIClient import OpenAIClient
from Simulator import Simulator
from SnippetGenerator import SnippetGenerator


class CodeCompletion:

    @staticmethod
    def complete(current_file, cursor_position, compare_method, path_to_repo):
        simulator = Simulator(path_to_repo)
        neighboring_files = simulator.get_neighboring_files(current_file)
        snippet_generator = SnippetGenerator(neighboring_files, 20, 60, current_file, cursor_position, compare_method)
        snippets = snippet_generator.get_snippets()
        context_generator = ContextGenerator(snippets, current_file, cursor_position, 3000)
        context = context_generator.generate_context()
        open_ai_client = OpenAIClient(context, program_parameter_open_ai_key)
        response = open_ai_client.submit_prompt()
        return response


############################################# Programmeinstieg ################################################

# Lesen der Programmparameter
program_parameter_path_to_repo = sys.argv[1]
program_parameter_current_file = sys.argv[2]
program_parameter_cursor_position = int(sys.argv[3])
program_parameter_open_ai_key = sys.argv[4]
program_parameter_compare_method = sys.argv[5]

# Generieren der Code-Vervollständigung
code_completion = CodeCompletion()
completion = code_completion.complete('r' + program_parameter_current_file,
                                      program_parameter_cursor_position,
                                      program_parameter_compare_method,
                                      'r' + program_parameter_path_to_repo)
