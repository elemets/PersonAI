import unittest
import sys
sys.path.append("..")
from Personality import Personality
import json

class PersonalityTest(unittest.TestCase):
    
        
    def setUp(self):
        self.Personality = Personality(["Dragonball Z"], ["Lord of the rings"], "swearing", "tester_char")
        
        
    def test_personality_calc_questions(self):
        
        sentence_scores, questions = self.Personality.personality_calc("I like Dragonball Z. What is your name?")
        
        self.assertEqual(questions, ["What is your name?"])
    
    def test_personality_calc_scores_pos(self):
        
        sentence_scores, questions = self.Personality.personality_calc("I like Dragonball Z. What is your name?")
        
        self.assertGreaterEqual(sum(sentence_scores), 0.2)
        
    def test_personality_calc_scores_neg(self):
        
                
        sentence_scores, questions = self.Personality.personality_calc("I hate Dragonball Z. What is your name?")
        
        self.assertLessEqual(sum(sentence_scores), -0.2)
        
    def test_increase_rating(self):
        
        self.Personality.increase_rating(5)
        
        self.assertEqual(self.Personality.personality_score, 5)
        
        with open("../Assets/Characters/tester_char.json") as f:
            tester_char_json= json.load(f)
            
        self.assertEqual(tester_char_json['Player_Rating'], 5)
        
        tester_char_json['Player_Rating'] = 0
        
        with open(f"../Assets/Characters/tester_char.json", "w") as f:
            json.dump(tester_char_json, f)
        
        f.close()        
        
    def test_decrease_rating(self):
        
        self.Personality.decrease_rating(-5)
        
        self.assertEqual(self.Personality.personality_score, -5)
            
             
        with open("../Assets/Characters/tester_char.json") as f:
            tester_char_json= json.load(f)
            
        self.assertEqual(tester_char_json['Player_Rating'], -5)

            
        tester_char_json['Player_Rating'] = 0
        
        with open(f"../Assets/Characters/tester_char.json", "w") as f:
            json.dump(tester_char_json, f)
        
        f.close()        
        
        
        

        

if __name__ == '__main__':
    unittest.main()