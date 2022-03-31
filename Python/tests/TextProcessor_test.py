import unittest
import sys
sys.path.append("..")
from TextProcessor import TextProcessor
import spacy 
import en_core_web_sm


class TextProcessorTest(unittest.TestCase):
    
    def setUp(self):
        self.textProcessor = TextProcessor()
    
    
    """ Testing several variations of split sentences"""
    def test_split_sentences_one(self):
                
        split_sentence = self.textProcessor.split_sentences("This sentence is a test")
        split_sentence_txt  = [ word.text for word in split_sentence]
        self.assertEqual(["This sentence is a test"], split_sentence_txt)
        
       
    def test_split_sentences_two(self):
                        
        split_sentence_multi = self.textProcessor.split_sentences("This sentence is a test. This is also a test.")
        split_sentence_multi_txt  = [ word.text for word in split_sentence_multi]
        self.assertEqual(["This sentence is a test.", "This is also a test."], split_sentence_multi_txt)
        
    def test_split_sentences_conj(self):
                         
        # textProcessor = TextProcessor()
        split_sentence_multi_conj = self.textProcessor.split_sentences("This sentence is a test. I love batman and superman.")
        split_sentence_multi_conj_txt =  [split_sentence_multi_conj[0].text , split_sentence_multi_conj[1], split_sentence_multi_conj[2]]
        self.assertEqual(["This sentence is a test.", "I love batman .", "I love superman"], split_sentence_multi_conj_txt)
        
    
    def test_positive_sentiment_check_test(self):
        in_sentence = "I love batman"
        self.assertGreaterEqual(self.textProcessor.sentiment_check(in_sentence), 0.2)
    
    def test_negative_sentiment_check_test(self):
  
        in_sentence = "I hate batman"
        self.assertLessEqual(self.textProcessor.sentiment_check(in_sentence), -0.2)
        
    def test_profanity_checker(self):
        in_sentence = "I fucking love batman"
        self.assertGreaterEqual(self.textProcessor.sentiment_check(in_sentence), 0.3)
        
        self.assertLessEqual(self.textProcessor.sentiment_check("this has no profanity"), 0)

if __name__ == '__main__':
    unittest.main()