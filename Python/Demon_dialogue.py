from pyparsing import countedArray
from Personality import Personality
import openai
import random
import json 
import wikipedia
import pandas as pd
from iteration_utilities import deepflatten
import re
from sparqlcuisinequery import cuisine_query, fictional_universe_query
"""
Demon class, this manages the demon's response to the player
"""

class Demon:

    def __init__(self, name, likes, dislikes, pref_speech, qa_pipeline):
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
        self.personality = Personality(self.likes, self.dislikes, pref_speech, name)
        
        self.qa_pipeline = qa_pipeline

    



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
    Returns the question response depending on whether the game creator
    has specified OpenAI or Transformers as the models for answering questions.
    """
    def question_answering(self, question, context):
        answers = {}
        with open(f'../Assets/Characters/{self.name}_context.json') as f:
            context = json.load(f)
            f.close()
        with open(f'../Assets/Character_Info/openai_filenames.json') as f:
            openai_files = json.load(f)  
        
        if self.Pers_Score > 25:
            true_context = context['context-very-liked']
            context_ai = 'very_liked'
        elif self.Pers_Score > 10:
            true_context = context['context-reasonably-liked']
            context_ai = 'reasonably_liked'
        else:
            true_context = context['context']
            context_ai = 'not_liked'
            

        if openai_files['open-ai'] == True:
            try:
                question = question[0]
                openai.api_key = str(openai_files['open-ai-api'])
                query = openai.Answer.create(
                    search_model="ada", 
                    model="curie", 
                    question=question, 
                    file=str(openai_files[self.name][context_ai]),
                    examples_context="In 2017, U.S. life expectancy was 78.6 years.", 
                    examples=[["What is human life expectancy in the United States?", "78 years."]], 
                    max_rerank=10,
                    max_tokens=40,
                    stop=["\n", "<|endoftext|>"]
                )
                
                answers['answer'] = query['answers'][0]
                answers['score'] = None
            except:
                answers['answer']  = random.choice(["I'm not sure I can help you with that...", "You'd be better off asking me something else", "This is not the information you're looking for..."])
                answers['score'] = None
        else:
            true_context = None
            
            print(self.Pers_Score)
           
                
            question = question[0]

            answers = self.qa_pipeline({
                'context': true_context,
                'question': question

            })
        return answers['answer'], answers['score']
            

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
                print(result['item'])
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
    