import asyncio
from numpy import character
import websockets
from Demon_dialogue import Demon
import json
import logging
from transformers import pipeline
from openai_helper import openai_init

### Logging set up
logger = logging.getLogger(__name__)  
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('DemonDetective.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class socket_server():
    
    def __init__(self):
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased-distilled-squad")
        with open("../Assets/Character_Info/character_names.json") as f:
            self.character_json = json.load(f) 
            self.num_of_characters = len(self.character_json['Characters'])
        self.current_demon = Demon(f'{self.character_json["Characters"]["Character_1"]}', ["nothing"], ["nothing"], "swearing", self.qa_pipeline)       
        self.character_dict = {}
        with open('../Assets/Character_Info/openai_filenames.json') as f:
            openai_check = json.load(f)
        if openai_check['open-ai'] == True and openai_check['already_initialised'] == False:
            openai_init()
        self.init_flag = False
    
    
    async def comms(self, websocket):
        output = "Nothing"
        type = "Null"
        pos_or_neg = "neutral"
        context = 'normal'
        prob_score = None
        init_counter = 0 
        async for message in websocket:

            message = message.decode('utf-8')
            message = json.loads(message)
            character_num = message['Name']
            demon_name = self.character_json['Characters'][character_num]
            instruction = message['Command']
            print(demon_name)
            print(character_num)
            if demon_name:
                with open("../Assets/Characters/" + demon_name + ".json") as file:
                    demon_info = json.load(file) 
            print(instruction)
            if instruction == 'init':
                print("Initialising with name ", demon_info['Name'])
                demon = Demon(demon_info['Name'], demon_info['Likes'], demon_info['Dislikes'], demon_info['Mannerisms'], self.qa_pipeline)       
                self.character_dict[f"{demon_info['Name']}"] = demon
                init_counter += 1
            
            sentence = message['Content']
            
            print(demon_name)
    
            if demon_info['Player_Rating'] > 8:
                context = "very-liked"
            elif demon_info['Player_Rating'] > 4:
                context = 'reasonably-liked'
            else:
                context = 'normal'

            if instruction == 'greet':
                output = self.character_dict[f'{demon_name}'].greet()
                type = "greet"
            elif instruction == 'response':
                output, pos_or_neg, prob_score = self.character_dict[f'{demon_name}'].respond(str(sentence), context)
                type = "response"
            elif instruction == 'get_score':
                output = demon_info['Player_Rating']            
         

            if init_counter == self.num_of_characters and not self.init_flag:
                type = "initialised"
                output = "None"
                self.init_flag = True

            data_to_be_sent = json.dumps({"Type": type, "Content": output, "Emotion": pos_or_neg, "prob_score": prob_score})
            logger.info(sentence)
            logger.info(data_to_be_sent)
            
            print(data_to_be_sent)
            await websocket.send(data_to_be_sent)
            
    async def main(self):
        async with websockets.serve(self.comms, "localhost", 1234):
            await asyncio.Future()

socket = socket_server()
asyncio.run(socket.main())