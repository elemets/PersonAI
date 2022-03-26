import openai
import json
from os import listdir

"""
This will upload the files to open ai using the supplied api key
and then save them in the openai_filenames json file ready to be used by the program.
"""
def openai_init():
    with open("../Assets/Character_Info/openai_filenames.json", "r+") as file:
        openai_filenames = json.load(file)    

    with open('../Assets/Character_Info/character_names.json') as charnamefile:
        character_names = json.load(charnamefile)
        charnamefile.close()

    context = ''
    context_reason = ''
    context_very = ''
    openai.api_key = openai_filenames['open-ai-api']
    ## creating the json lines files out the context files supplied
    for character in character_names['Characters'].values():
        
        with open(f'../Assets/Characters/{character}_context.json') as context_file:
            contexts = json.load(context_file)
        
        with open(f'../Assets/Characters/openaijsonl/{character}_not_liked.jsonl', "w") as f:
            context = {"text": contexts['context'] }
            json.dump(context, f)
            f.close()
        
        with open(f'../Assets/Characters/openaijsonl/{character}_reasonably_liked.jsonl', "w") as f:
            context_reason = {"text": contexts['context-reasonably-liked'] }
            json.dump(context_reason, f)
            f.close()
            
        with open(f'../Assets/Characters/openaijsonl/{character}_very_liked.jsonl', "w") as f:
            context_very = {"text": contexts['context-very-liked'] }
            json.dump(context_very, f)
            f.close()
        
        ## uploading the files
        file_not = openai.File.create(file=open(f'../Assets/Characters/openaijsonl/{character}_not_liked.jsonl'), purpose='answers') 
        file_reasonably = openai.File.create(file=open(f'../Assets/Characters/openaijsonl/{character}_reasonably_liked.jsonl'), purpose='answers') 
        file_very = openai.File.create(file=open(f'../Assets/Characters/openaijsonl/{character}_very_liked.jsonl'), purpose='answers') 

        ## adding them to the json
        openai_filenames[f'{character}'] = {}
        openai_filenames[f'{character}']['not_liked'] = file_not['id']
        openai_filenames[f'{character}']['reasonably_liked'] = file_reasonably['id']
        openai_filenames[f'{character}']['very_liked'] = file_very['id']

    openai_filenames['already_initialised'] = True
    with open("../Assets/Character_Info/openai_filenames.json", "r+") as file:
        json.dump(openai_filenames, file)
    print("Open ai files initialised")
    
def file_deleter():
    with open("../Assets/Character_Info/openai_filenames.json", "r+") as file:
        openai_filenames = json.load(file)
    with open('../Assets/Character_Info/character_names.json') as charnamefile:
        character_names = json.load(charnamefile)
    
    openai.api_key = openai_filenames['open-ai-api']

    file_id_list = []
    for character in character_names['Characters'].values():
        
        if character in openai_filenames:
            file_id_list.append(openai_filenames[character]["not_liked"])
            file_id_list.append(openai_filenames[character]["reasonably_liked"])
            file_id_list.append(openai_filenames[character]["very_liked"])
            del openai_filenames[character]
    
    for id in file_id_list:
        openai.File.delete(id)
    
    openai_filenames['already-intialised'] = False
    
    with open("../Assets/Character_Info/openai_filenames.json", "r+") as file:
        json.dump(openai_filenames, file)
        