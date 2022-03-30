import unittest
import sys
sys.path.append("..")
from TextProcessor import TextProcessor
import spacy 
import en_core_web_sm


class TextProcessorTest(unittest.TestCase):
    
    
    def test_split_sentences(self):
        
        nlp = en_core_web_sm.load()
        textProcessor = TextProcessor()
        split_sentence = textProcessor.split_sentences("This sentence is a test")
        split_sentence_txt  = [ word.text for word in split_sentence]
        self.assertEqual(["This sentence is a test"], split_sentence_txt)
        
if __name__ == '__main__':
    unittest.main()