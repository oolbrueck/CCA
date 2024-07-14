import unittest
from unittest.mock import patch
from SnippetGenerator import SnippetGenerator

class TestSnippetGenerator(unittest.TestCase):
    def setUp(self):
        self.neighboringFiles = {
            'fileRelatedToParentClass': ['parent_class_file.py'],
            'filesRelatedToSiblingsClasses': ['sibling_class_file.py'],
            'fileRelatedToImportedClasses': ['imported_class_file.py'],
            'fileRelatedToClassesFromNeighboringFiles': ['neighboring_class_file.py']
        }
        focussed_file = "./repos/dir1/dir2/Foo.java"
        self.generator = SnippetGenerator(self.neighboringFiles, 10, 10, focussed_file, 29, 'jaccard')

    def test_tokenize_code(self):
        code = """
        public class MainClass {
            public static void main(String[] args){
                System.out.println("Hello World");
            }
        }
        """

        expected_tokens = ['public', 'class', 'MainClass', '{', 'public', 'static', 'void', 'main', '(', 'String', '[',
                           ']', 'args', ')', '{', 'System', '.', 'out', '.', 'println', '(', 'Hello', 'World', ')', ';', '}', '}']

        self.assertEqual(self.generator._SnippetGenerator__tokenize_code(code), expected_tokens)


    def test_filter_windows_of_specific_file(self):
        windows_of_specific_file = [
            {'value': 0.6, 'range': [0, 10]},
            {'value': 0.8, 'range': [5, 15]},
            {'value': 0.4, 'range': [10, 20]},
            {'value': 0.7, 'range': [20, 30]},
            {'value': 0.9, 'range': [25, 35]}
        ]
        expected_filtered_windows = [{'value': 0.9, 'range': [25, 34]},
                                     {'value': 0.8, 'range': [5, 14]}]

        filtered_windows = self.generator._SnippetGenerator__filter_windows_of_specific_file(windows_of_specific_file)
        self.assertEqual(filtered_windows, expected_filtered_windows)

    def test_get_code_from_domain_window(self):
        code = """
                    } catch (Exception e) {
            System.err.println("Error creating Word file: " + e.getMessage());
        }
    }
    public void createParagraph() {

    }
    public void createPdfFile(String text, int fontSize) {
        // Create a new document
        Document document = new Document();
        // Create a paragraph
        """

        self.assertEqual(self.generator._SnippetGenerator__get_code_from_domain_window(), self.generator._JaccardSnippetGenerator__get_code_from_domain_window()) #TODO

if __name__ == '__main__':
    unittest.main()
