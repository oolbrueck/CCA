import sys

from ContextGenerator import ContextGenerator
from OpenAIClient import OpenAIClient
from Protocol import protocol_obj
from Simulator import Simulator
from SnippetGenerator import SnippetGenerator


class CodeCompletion:

    @staticmethod
    def complete():
        simulator = Simulator(program_parameter_path_to_repo)
        neighboring_files = simulator.get_neighboring_files(program_parameter_current_file)
        snippet_generator = SnippetGenerator(neighboring_files,
                                             program_parameter_domain_window_size,
                                             program_parameter_co_domain_window_size,
                                             program_parameter_current_file,
                                             program_parameter_cursor_position,
                                             program_parameter_compare_method,
                                             program_parameter_intersection_threshold,
                                             program_parameter_value_threshold)
        snippets = snippet_generator.get_snippets()
        context_generator = ContextGenerator(snippets, program_parameter_current_file, program_parameter_cursor_position, program_parameter_context_token_limit)
        context = context_generator.generate_context()
        open_ai_client = OpenAIClient(context, program_parameter_open_ai_key, program_parameter_model)
        response = open_ai_client.submit_prompt()
        return response


############################################# Programmeinstieg ################################################

# Lesen der Programmparameter
program_parameter_path_to_repo = sys.argv[1]
program_parameter_current_file = sys.argv[2]
program_parameter_cursor_position = int(sys.argv[3])
program_parameter_open_ai_key = sys.argv[4]
program_parameter_compare_method = sys.argv[5]
program_parameter_domain_window_size = int(sys.argv[6])
program_parameter_co_domain_window_size = int(sys.argv[7])
program_parameter_context_token_limit = int(sys.argv[8])
program_parameter_intersection_threshold = float(sys.argv[9])
program_parameter_value_threshold = float(sys.argv[10])
program_parameter_model = sys.argv[11]
program_parameter_original_code = sys.argv[12]

# Setzen der Programmparameter im Protokoll
protocol_obj.program_parameters['path_to_repo'] = program_parameter_path_to_repo
protocol_obj.program_parameters['current_file'] = program_parameter_current_file
protocol_obj.program_parameters['cursor_position'] = program_parameter_cursor_position
protocol_obj.program_parameters['compare_method'] = program_parameter_compare_method
protocol_obj.program_parameters['domain_window_size'] = program_parameter_domain_window_size
protocol_obj.program_parameters['co_domain_window_size'] = program_parameter_co_domain_window_size
protocol_obj.program_parameters['context_token_limit'] = program_parameter_context_token_limit
protocol_obj.program_parameters['intersection_threshold'] = program_parameter_intersection_threshold
protocol_obj.program_parameters['value_threshold'] = program_parameter_value_threshold
protocol_obj.program_parameters['model'] = program_parameter_model
protocol_obj.program_parameters['original_code'] = program_parameter_original_code

# Generieren der Code-Vervollständigung
code_completion = CodeCompletion()
completion = code_completion.complete()

protocol_obj.completion = completion

print(protocol_obj.completion)

#TODO
# calculate the codebleau score between the original code and the completion
# codebleu_score = calculate_code_bleu_score(program_parameter_original_code, completion)
# protocol_obj.code_bleu_score = codebleu_score

