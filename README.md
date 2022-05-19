
# Sword In The Stone

### Requirements

Python (with libraries), Godot (with OSAsync)

Requirements can be found in the requirements.txt file in the root of the project for the python part of the project.

Godot also needs to have the OSAsync plugin installed.

### Assets

In order to turn this game into another project look in the /Assets/ folder here you will find a layout which looks somewhat like this:

Looking inside these folders will help you understand the way the files need to be formatted

Each character needs:

- Expression images (Happy, Sad, Neutral)
- To exist within character_names.json (along with the number of hframes and vframes if an animation .png is used)
- A sprite which is displayed in the game world (preferably 32x32 but will be resized)
- {character_1_name}.json e.g. Artorius.json which contains their name, likes, dislikes, whether they prefer swearing or not, and Food_Bool which should be set to false at the start
- If the likes contain a like such as:
    - Greece Food or England Food
    - The game will look up cuisines from this country add it to a list of likes and then set the Food_Bool to True so that it doesn’t do this every time.

Assets File System:

- Character_Info
    - character_names.json
    - openai_filenames.json
- Characters
    - Character_1
        - Expressions
            - Happy.png
            - Sad.png
            - Neutral.png
        - Character_1_Sprite.png
    - {character_1_name}.json
    - {character_1_name}_responses.json
    - {character_1_name}_context.json
    - and so on for up to 4 characters
- DialogRoom
    - background.jpg (background for dialog room)
    - custom_font.otf (font to be used throughout your game)
- FinalRoom
    - Final_Button.png (These images are attached to the buttons to navigate through the final room menus)
    - Next_Button.png (These both have pressed versions which display when pressed)
    - FinalRoomBackground.png (The final room background)
    - parchment.png (The text is displayed on this in the final room)
- Floor
    - floorboards.png (The ground texture can be anything not just floorboards)
- InfoJSONs
    - final_screen.json
        - Contains:
            - Text to be displayed on the final screen before the player inputs their questions e.g “The court will now hear your testimony...”
            - Between 1 and 4 questions with correct answers
            - winning and losing screen text displayed when a player wins or loses.
    - information_screen.json
        - Contains:
            - Introduction to your game explaining the premise and the questions the player needs to answer at the end
            - Controls explanation
- IntroRoom
    - background.jpg
- MainRoom
    - imreadybutton.png (this is the button which will take you from the main room to the final screen room)
    - imreadypressed.png
- sparqlJSONs (choose the fictional universe or countries you want to select likes and dislikes from these)
    - all_fictional_universes.json
    - Country_Labels.json
- WallsTileMap.png
    - Contains 4 wall tiles for the back walls of the main room
- Player.png (the player sprite)
