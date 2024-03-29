from this import s
from pyparsing import countedArray
from Personality import Personality
from TextProcessor import TextProcessor
import openai
import random
import json 
from sentence_transformers import util
from collections import OrderedDict
import numpy as np
import spacy
from iteration_utilities import deepflatten
from sparqlcuisinequery import cuisine_query, fictional_universe_query
"""
Demon class, this manages the demon's response to the player
"""

class Demon:

    def __init__(self, name, likes, dislikes, pref_speech, similarity_model, text_processor):
        self.name = name
        with open(f'../Assets/Characters/{name}_responses.json') as f:
            data = json.load(f)
        self.dialogue = data
        self.likes = likes
        self.dislikes = dislikes
        ### section deals with a demon liking a specific cuisine
        self.food_lookup_bool = False
        self.Pers_Score = 0 
        with open(f'../Assets/Characters/{name}.json') as f:
            demon_info = json.load(f)
        print(demon_info['Food_Bool'])
        if not demon_info['Food_Bool'] and self.likes[0] != 'nothing': 
            new_likes  = self.food_universe_lookup(likes)
            new_dislikes = self.food_universe_lookup(dislikes)
            print(self.dislikes)
            print(new_dislikes)
            self.dislikes = self.dislikes + new_dislikes
            self.likes = self.likes + new_likes
            with open(f'../Assets/Characters/{name}.json', "w") as f:
                demon_info['Likes'] = self.likes
                demon_info['Dislikes'] = self.dislikes
                demon_info['Food_Bool'] = self.food_lookup_bool
                json.dump(demon_info, f)
        
        self.Pers_Score = demon_info['Player_Rating']
        self.personality = Personality(self.likes, self.dislikes, pref_speech, name, text_processor)
        
        self.similarity_model = similarity_model
        self.asked_questions = OrderedDict()
        self.nlp = spacy.load('en_core_web_lg')
        self.text_processor = text_processor
        self.question_set = {
            "Who is your favourite director?", 
            "What is your favourite sport?",
            "What sort of music do you listen to?",
            "What genre of films do you like?",
        }
        with open(f'../Assets/Character_Info/openai_filenames.json') as f:
            openai_files = json.load(f)  
        openai.api_key = str(openai_files['open-ai-api'])

        
    
    """
    Calculates the response given the player input and context (if using transformers)
    """
    def calc_response(self, player_input, context):

        ## calculating the scores of the players personality
        personality_scores, questions = self.personality.personality_calc(player_input)
        ## calculate mean of the scores
        mean_score = sum(personality_scores) / len(personality_scores)
        

        pos_or_neg = None
        prob_score = None
        
        if mean_score > 0.3:
            response = self.positive_response(mean_score)
            pos_or_neg = "pos"
        elif mean_score < -0.1:
            response = self.negative_response(mean_score)
            pos_or_neg = "neg"
        else:
            response = self.neutral_response()
            pos_or_neg = "neutral"
            
        if questions:
            response, prob_score = self.question_answering(questions, context)
        
        return response, pos_or_neg, prob_score

    """
    Returns 
    the question response depending on whether the game creator
    has specified OpenAI or Transformers as the models for answering questions.
    """
    def question_answering(self, question, context):
        
        question = question[0]
        
        answers = {}
        with open(f'../Assets/Characters/{self.name}_context.json') as f:
            context = json.load(f)
            f.close()
            
            

            
        
        if self.Pers_Score > 10:
            true_context = context['context-very-liked']
            context_ai = 'very_liked'
        elif self.Pers_Score > 5:
            true_context = context['context-reasonably-liked']
            context_ai = 'reasonably_liked'
        else:
            true_context = context['context']
            context_ai = 'not_liked'
            

        try:
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Context: {true_context}, Give a long and opinionated answer to this question using the context provided above (but also make some stuff up): {question}",
            temperature=0.75,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            )
            print(response)
            print(f"Context: {true_context}, \n Q: {question}")
            answer_to_return = response['choices'][0]['text'].replace("\n", "")
            answers['score'] = None
        except:
            answers['score'] = None
            answer_to_return = random.choice(["I'm not sure I can help you with that...", "You'd be better off asking me something else", "This is not the information you're looking for..."])
        

        #### SIMILARITY CHECK
        ## check for similarity
        ## if similar check for sentiment on sentence
        ## if similarity and sentiment are close enough then increment the counter and respond accordingly
        sim_enough = False
        current_question = self.nlp(question)
        # sim_questions = {current_question.similarity(self.nlp(question)):question for question in self.asked_questions}
        if self.asked_questions:
            question_list = list(self.asked_questions.keys())
            current_question_emb = self.similarity_model.encode(question)
            ### embed the questions compare them and then assign a dictionary with the similarity score as the key and question as value
            sim_questions = {util.cos_sim(current_question_emb, self.similarity_model.encode(question)): question for question in question_list}
            
            
        if self.asked_questions:
            sim_enough = max(sim_questions) > 0.85
            most_sim_question = sim_questions[max(sim_questions)]
            print(sim_questions)
            already_asked = self.asked_questions[most_sim_question][1] == 1
            answer_to_return = current_question
            if sim_enough and not already_asked:
                self.asked_questions[most_sim_question] = (self.asked_questions[most_sim_question][0], 1)
                answer_to_return = f"You've already asked me this, but... {self.asked_questions[most_sim_question][0]}"
            elif sim_enough and already_asked:
                answer_to_return = "Stop asking me that!"
            else:
                self.asked_questions[question] = (answer_to_return, 0)
        else:
            self.asked_questions[question] = (answer_to_return, 0)
                    
        if len(self.asked_questions) > 1000:
            self.asked_questions.popitem()


        #### TYPE OF QUESTION CHECK
        ## check type of question
        ## if opinion check if nouns within question exist within likes and dislikes file
        ## if any do not add to the likes and dislikes 
        ## only do this if the question hasn't been asked before
        

        question_type = self.question_check(question)
        
        
        if question_type == 'Opinion' and not sim_enough:
            question_noun = self.text_processor.question_noun_extractor(question)
            nouns = self.text_processor.noun_extractor(answer_to_return)
            self.like_dislike_extractor(nouns, question_noun)


        return answer_to_return, answers['score']
            
        
    """
    Checking the type of question asked by the player 
    """    
    def question_check(self, question):
        opin_resp = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Classify this question into fact or opinion using these as examples only provide the classification\n\nExample Questions:\nWhat sports do you like?\nHow tall is Shaq?\nWho is your favourite author?\nWhat is the best sushi restaurant?\nWhat is sushi?\n\nExample Classifications:\nOpinion\nFact\nOpinion\nOpinion\nFact\n\nQuestion:\n{question}\n\nClassification:\n",
            temperature=0,
            max_tokens=64,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        fact_or_opin = opin_resp['choices'][0]['text'].strip()
        print(fact_or_opin)
        
        return fact_or_opin
        
        
        
    def like_dislike_extractor(self, nouns, question_noun):
        
        if question_noun:
            question_noun = question_noun[0]
            for noun, sent in nouns.items():
                like_dis = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"Is this word related to a {question_noun} (answer Yes or No):\n1. {noun}\nAnswer:\n",
                    temperature=0,
                    max_tokens=3,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                yes_or_no = like_dis['choices'][0]['text'].strip()
                print("YES OR NO")
                print(yes_or_no)
                if yes_or_no == 'Yes':
                    if sent == 'pos':
                        old_likes = self.likes
                        self.likes += [noun]
                    if sent == 'neg':
                        self.dislikes += [noun]
                
    
    """
    If the noun is related to the question noun e.g. the demon asks what sort of music do you like 
    and you answer Jazz then it will decide on whether it likes jazz or not
    """
    def like_dislike_extract_no_add(self, nouns, question_noun):
        noun_opinion_pair = []
        
        print(nouns)
        print(question_noun)
        if question_noun:
                    for noun in nouns.items():
                        like_dis = openai.Completion.create(
                            model="text-davinci-003",
                            prompt=f"Is this word related to a {question_noun[0]} (answer Yes or No):\n{noun[0]}\nanswer:\n",
                            temperature=0,
                            max_tokens=3,
                            top_p=1.0,
                            frequency_penalty=0.0,
                            presence_penalty=0.0
                        )
                        print("+++++ Nouns and Q Noun 0 ++++++")
                        print(noun[0])
                        print(question_noun[0])
                        yes_or_no = like_dis['choices'][0]['text'].strip()
                        if yes_or_no == 'Yes':
                            if random.choice([True, False]):
                                self.likes += noun[0]
                                noun_opinion_pair += (noun[0], "positive")
                            else:
                                self.dislikes += noun[0]
                                noun_opinion_pair += (noun[0], "negative")

        return noun_opinion_pair

    """
    Will ask a random question then we need to get the response decide an opinion of the players response 
    if a question has just been asked then the noun extractor is required
    once the correct noun is found then the demon can decide whether to like or dislike this and thus form an 
    opinion on it 
    Maybe instead of a period of time the random questions should be tagged onto the end of the text 
    Probably a better idea but one for later
    """
    def question_asker(self):
        if self.question_set:
            demon_question_to_ask = random.choice(tuple(self.question_set))
            self.question_set.remove(demon_question_to_ask)
        else:
            demon_question_to_ask = ''
        return demon_question_to_ask
    
    """
    Responding once a question has been asked this needs to be called
    """
    def question_respond(self, response, question):
        ## first find the noun within the response
        question_noun = self.text_processor.question_noun_extractor(question)
        nouns = self.text_processor.noun_extractor(response)
        ## added opinions to like and dislike
        ## now a response is required in order to make the conversation convincing

        nouns = {noun: op for noun, op in nouns.items() if noun not in question_noun}
        noun_op_pairing = self.like_dislike_extract_no_add(nouns, question_noun)
        
        print(f"Noun, Op Pair: {noun_op_pairing}")

        
        
        if len(noun_op_pairing) >= 6:
            answer_regarding_question = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Write a few sentences about these nouns forming your own opinion using this noun and opinion pair, using the opinion component to guide your sentence \n {noun_op_pairing[0]} - {noun_op_pairing[1]} \n {noun_op_pairing[2]} - {noun_op_pairing[3]} \n {noun_op_pairing[4]} - {noun_op_pairing[5]}",
                temperature=1,
                max_tokens=246,
                top_p=1.0,
                frequency_penalty=0.1,
                presence_penalty=0.49
            )
            answer_to_q_return = answer_regarding_question['choices'][0]['text']  

        elif len(noun_op_pairing) == 4:
            answer_regarding_question = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Write a few sentences about these nouns forming your own opinion using this noun and opinion pair, using the opinion component to guide your sentence \n {noun_op_pairing[0]} - {noun_op_pairing[1]} \n {noun_op_pairing[2]} - {noun_op_pairing[3]} \n ",
                temperature=1,
                max_tokens=256,
                top_p=1.0,
                frequency_penalty=0.1,
                presence_penalty=0.49
            )
            answer_to_q_return = answer_regarding_question['choices'][0]['text']  

        elif (len(noun_op_pairing) == 2):
            answer_regarding_question = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Write a few sentences about these nouns forming your own opinion using this noun and opinion pair, using the opinion component to guide your sentence\n {noun_op_pairing[0]} - {noun_op_pairing[1]}",
                temperature=1,
                max_tokens=256,
                top_p=1.0,
                frequency_penalty=0.1,
                presence_penalty=0.49
            )
            answer_to_q_return = answer_regarding_question['choices'][0]['text']  
        else:
            answer_to_q_return = "I don't think what you said was relevant to my question. I'm bored ask me something!"
       

        return answer_to_q_return


    """
    Ending where demons who lied come back to roast you
    This can be done by checking where the player was in the context with the demons
    """
    ## grabbing random greeting out of greeting list for demon
    def greet(self):

        greeting = self.dialogue['Greetings'][random.randint(0, len(self.dialogue['Greetings']) -1 )]
        return greeting


    """
    If trigger word is typed in and the player knows """
    def respond(self, player_input, context):
        pos_or_neg = None
        if "Tell me what you know." in player_input and self.Pers_Score > 5:
            resp = self.dialogue['Clues']['success'][random.randint(0, len(self.dialogue['Clues']['success']) - 1)]
            pos_or_neg = "pos"
        elif "Tell me what you know." in player_input:
            resp = self.dialogue['Clues']['failure'][random.randint(0, len(self.dialogue['Clues']['failure']) - 1)]
            pos_or_neg = "neg"
        else:
            resp, pos_or_neg, prob_sore = self.calc_response(player_input, context)
        return resp, pos_or_neg, prob_sore

    def negative_response(self, decrease_amount):
        self.personality.decrease_rating(decrease_amount)
        resp = self.dialogue['Reactions']['negative'][random.randint(0, len(self.dialogue['Reactions']['negative']) - 1)]
        return resp

    def positive_response(self, increase_amount):
        self.personality.increase_rating(increase_amount)
        resp = self.dialogue['Reactions']['positive'][random.randint(0, len(self.dialogue['Reactions']['positive']) - 1)]
        return resp

    def neutral_response(self):
        resp = self.dialogue['Reactions']['neutral'][random.randint(0, len(self.dialogue['Reactions']['neutral']) - 1)]
        return resp

    def personality_score(self):
        return self.personality.personality_score
    
    """
    Takes the list of likes or dislikes and checks it for 
    key word food, if it contains food then it will append
    all the dishes from wikidata query.
    This now also does the same for any fictional universes in the likes """
    def food_universe_lookup(self, likes_or_dislikes):
        likes_or_dislikes_to_add = []
        dish_names = []
        ## finds all likes with the word food in it...
        likes_with_food_in = [like for like in likes_or_dislikes if "food" in like]
        likes_without = [like.replace("food", "") for like in likes_with_food_in]
        
        ## finds any likes which match any of the fictional universes
        with open("../Assets/sparqlJSONS/all_fictional_universes.json") as file:
            fictional_universes = json.load(file)
        fictional_universe_ids = []
        ## finds the id within the list of dictionaries
        ## appends them to universe ids list
        for result in fictional_universes:
            if result['itemLabel'] in likes_or_dislikes:
                fictional_universe_ids.append(result['item'])
        if likes_with_food_in != None:
            self.food_lookup_bool = True
        if fictional_universe_ids != None:
            self.universe_lookup_bool = True
        
        universe_character_list = []
        for universe in fictional_universe_ids:
            universe_character_list += fictional_universe_query(universe)
        for cuisine_likes in likes_without:
            cuisine_id = self.cuisine_lookup(cuisine_likes)
            dishes = cuisine_query(cuisine_id)
            dish_names.append(dishes)
        print(universe_character_list)
        dish_names = self.flatten(dish_names)
        
        likes_or_dislikes_to_add = dish_names + universe_character_list
        return likes_or_dislikes_to_add
    
    def flatten(self, t):
        return list(deepflatten(t, depth=1))

    def cuisine_lookup(self, country):
        with open("../Assets/sparqlJSONS/Country_Labels.json") as f:
            id_country_list = json.load(f)
        country_id = ''
        for country_dict in id_country_list:
            if str(country_dict['itemLabel']).casefold() in str(country).casefold():
                country_id = country_dict['item']
        return country_id
    