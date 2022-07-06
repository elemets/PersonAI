
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from profanity_check import predict_prob
from collections import Counter
import en_core_web_sm

"""
TextProcessor
This deals with the nlp techniques used in
the Personality class
"""
class TextProcessor:

    def __init__(self):
        # self.Profanity = ProfanityFilter()
    
        self.tag_list = ["nsubj", "ROOT", "conj"]
        self.nlp =en_core_web_sm.load()

        # self.prof_filter = ProfanityFilter()
        

    """
    Splits the sentences and splits conjunctions correctly
    This allows people to enter sentences such as 'I love batman and superman'
    and splits this to 'I love batman. I love superman'.
    This allows the system to deal with a dislike and a like being within the same sentence 
    and it can still infer the correct sentiment score from this.
    """
    def split_sentences(self, raw_text):
        

        
        # nlp.add_pipe("sentencizer")

        doc = self.nlp(raw_text)
        short_conj_sentence = False

        sentence_list = list(doc.sents)
        ## grab the sentence before
        for sentence in range(len(sentence_list)):
            ## Counting the different number of POS tags in a sentence
            pos_counts = Counter([word.pos_ for word in sentence_list[sentence]])

            for index, word in enumerate(sentence_list[sentence]):
                ##if word.dep_ is conj then grab the root and nsubj in sentence

                ## checking if it matches the shorter sentence clause
                if pos_counts['VERB'] < 2:
                    short_conj_sentence = True 

                ## if it matches specific type of "and" conjunction then we can split into two sentences
                ## this handles very basic I like this and that and splits it into 
                ## I like this and this
                if word.dep_ == 'cc' and str(word) == 'and' and short_conj_sentence:
                    
                    new_sentence = [word.text for word in sentence_list[sentence] if word.dep_ in self.tag_list ]
                    new_sentence = ' '.join(new_sentence)
                    sentence_list.append(new_sentence)
                    original_sentence = [word.text for word in sentence_list[sentence]]
                    edited_old_sentence = [word.text for word in sentence_list[sentence] if word.dep_ == 'conj' or word.dep_ == 'cc']
                    original_new = [word for word in original_sentence if word not in edited_old_sentence]
                    sentence_list[sentence] = ' '.join(original_new)

                elif word.dep_ == 'cc':

                    new_sentence = str(sentence_list[sentence]).split(str(word))
                    sentence_list[sentence] = new_sentence[0]
                    sentence_list.append(new_sentence[1])
                    

        return sentence_list


    def noun_extractor(self, raw_sentences):
        
        doc = self.nlp(raw_sentences)
        
        sentence_list = list(doc.sents)
        ## new sentences where there are conjugations
        for sentence in range(len(sentence_list)):
            for index, word in enumerate(sentence_list[sentence]):
                
                if word.pos_ == 'CCONJ':
                    word = self.nlp.tokenizer(".")

        
        ## finding the sentiment of the sentences
        for sentence in range(len(sentence_list)):
            sentence_sent = str(sentence_list[sentence])
            sentence_sent = self.sentiment_check(sentence_sent)
            print(sentence_sent)
            if sentence_sent > 0.3:
                ## pos
                for index, word in enumerate(sentence_list[sentence]):
                    if word.pos_ == 'NOUN':
                        ## add it to list of likes 
                        print(word)
            elif sentence_sent < -0.3:
                for index, word in enumerate(sentence_list[sentence]):
                    if word.pos_ == 'NOUN':
                        ## add it to list of dislikes 
                        print(word)
                ## neg
            

        
        
        
                

    """
    Checking the sentiment of the given sentence
    """
    def sentiment_check(self, sentence):

        sentAnalyzer = SentimentIntensityAnalyzer()
        
        ## returning the compound sentiment from a sentence
        sentiment = sentAnalyzer.polarity_scores(sentence)['compound']

        return sentiment


    """
    Returning the probability that the given sentence contains profanity
    """
    def profanity_checker(self, sentence):
        sentence = [sentence]
        
        
        return predict_prob(sentence)