from TextProcessor import TextProcessor
import json

class Personality:

    """
    likes: whatever this personality likes e.g. a book, another character or even a shape
    dislikes: the opposite of likes
    pref_speech: the preferred manner of speech, could be formal, informal, no expletives etc.
    personality_score: this determines how much this instance of demon likes you. Ranging from 
    - 10 to 10, always starts at 0. 
    """
    def __init__(self, likes, dislikes, pref_speech, name):

        self.likes = likes
        self.dislikes = dislikes
        self.name = name
        self.pref_speech = pref_speech
        with open(f"../Assets/Characters/{name}.json") as file:
            self.json_file = json.load(file)
        self.personality_score = self.json_file['Player_Rating']
        self.textProcessor = TextProcessor()
    

    """
    This function will check for the occurance of any of the 
    characters dislikes or likes in the input text.
    This can then be used by sentiment analysis to detect whether
    they are being positive or negative about a certain keyword.
    """
    def personality_calc(self, corpus):
        

        sentences = self.textProcessor.split_sentences(corpus)

        ## checking each sentence for likes and dislikes to work out 
        ## the sentiment for each sentence as well as the subject (hopefully)
        sentence_scores = []
        questions = []
        for sentence in sentences:
            try:
                if '?' in sentence.text:
                    questions.append(sentence.text)
            except:
                if '?' in sentence:
                    questions.append(sentence)

            dislike_score = []
            like_score = []
            try:
                sentence = [word.text for word in sentence]
                sentence = " ".join(sentence)
            except:
                pass

            sentence = sentence.casefold()
            dislike_score = sum(self.score_analyser("dislike", sentence))
            like_score = sum(self.score_analyser("like", sentence))
           
            
            sentence_scores.append(dislike_score + like_score)
                
            

        return sentence_scores, questions

    def increase_rating(self, increase_amount):
        self.json_file["Player_Rating"] += increase_amount
        self.json_file['Player_Rating'] = float(self.json_file['Player_Rating'])
        with open(f"./Demons/{self.name}.json", "w") as f:
            json.dump(self.json_file, f)
        self.personality_score += increase_amount


    def decrease_rating(self, decrease_amount):
        self.json_file["Player_Rating"] += decrease_amount
        self.json_file['Player_Rating'] = float(self.json_file['Player_Rating'])
        with open(f"./Demons/{self.name}.json", "w") as f:
            json.dump(self.json_file, f)
        self.personality_score += decrease_amount

    def score_analyser(self, like_or_dislike, sentence):
        if like_or_dislike == 'like':
            opinion = self.likes
        else:
            opinion = self.dislikes
            
        profanity_check = self.textProcessor.profanity_checker(sentence)

        opinion_score = []
        for op in opinion:
            op = op.casefold()
            sentiment_value = 0
            if op in str(sentence):
                
                sentiment_value = self.textProcessor.sentiment_check(sentence)
                if self.pref_speech == 'no_swearing':
                    sentiment_value = sentiment_value * (1 - profanity_check)
                elif self.pref_speech == 'swearing':
                    sentiment_value = sentiment_value * (1 + profanity_check)
                    
                    
            if like_or_dislike == 'dislike':
                sentiment_value = -sentiment_value

            ## setting sentiment_valuescore to 0 
            opinion_score.append(sentiment_value)
        return opinion_score
            
            