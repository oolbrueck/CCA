import unittest
from unittest.mock import patch
from JaccardSnippetGenerator import JaccardSnippetGenerator

class TestJaccardSnippetGenerator(unittest.TestCase):
    def setUp(self):
        self.neighboringFiles = {
            'fileRelatedToParentClass': ['parent_class_file.py'],
            'filesRelatedToSiblingsClasses': ['sibling_class_file.py'],
            'fileRelatedToImportedClasses': ['imported_class_file.py'],
            'fileRelatedToClassesFromNeighboringFiles': ['neighboring_class_file.py']
        }
        focussedFile = "./repos/dir1/dir2/Foo.java"
        self.generator = JaccardSnippetGenerator(self.neighboringFiles, 10, 10, focussedFile, 29)

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

        self.assertEqual(self.generator._JaccardSnippetGenerator__tokenizeCode(code), expected_tokens)


    def test_filter_windows_of_specific_file(self):
        windowsOfSpecificFile = [
            {'jaccardValue': 0.6, 'range': [0, 10]},
            {'jaccardValue': 0.8, 'range': [5, 15]},
            {'jaccardValue': 0.4, 'range': [10, 20]},
            {'jaccardValue': 0.7, 'range': [20, 30]},
            {'jaccardValue': 0.9, 'range': [25, 35]}
        ]
        expected_filtered_windows = [{'jaccardValue': 0.9, 'range': [25, 34]},
                                     {'jaccardValue': 0.8, 'range': [5, 14]}]

        filtered_windows = self.generator._JaccardSnippetGenerator__filterWindowsOfSpecificFile(windowsOfSpecificFile)
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

        self.assertEqual(self.generator._JaccardSnippetGenerator__getCodeFromDomainWindow(), self.generator._JaccardSnippetGenerator__getCodeFromDomainWindow()) #TODO

if __name__ == '__main__':
    unittest.main()
