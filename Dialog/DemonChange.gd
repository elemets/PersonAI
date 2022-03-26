extends Sprite


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var demon_name = 'Magdela'
var texture_string
var current_character = 'Character_1'
# Called when the node enters the scene tree for the first time.
func _ready():
	texture_string = "./Assets/Characters/"+  current_character + "/Expressions/Happy.png"
	texture = load(texture_string)
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_RichTextLabel_mood(emotion):
	print("emotion received")
	print(emotion)
	if emotion == 'pos':
		texture_string = "./Assets/Characters/"+current_character+"/Expressions/Happy.png"
		texture = load(texture_string)
	elif emotion == 'neg':
		texture_string = "./Assets/Characters/"+current_character+"/Expressions/Sad.png"
		texture = load(texture_string)
	else:
		texture_string = "./Assets/Characters/"+current_character+"/Expressions/Neutral.png"
		texture = load(texture_string)
	pass # Replace with function body.



func _on_Character_2_conversation(demon_name):
	demon_name = demon_name
	texture_string = "./Assets/Characters/Character_2/Expressions/Happy.png"
	current_character = "Character_2"
	texture = load(texture_string)
	pass 


func _on_Character_1_conversation(demon_name):
	demon_name = demon_name
	texture_string = "./Assets/Characters/Character_1/Expressions/Happy.png"
	current_character = "Character_1"
	texture = load(texture_string)
	pass 


func _on_Character_3_conversation(demon_name):
	demon_name = demon_name
	texture_string = "./Assets/Characters/Character_1/Expressions/Happy.png"
	current_character = "Character_3"
	texture = load(texture_string)
	pass # Replace with function body.


func _on_Character_4_conversation(demon_name):
	demon_name = demon_name
	texture_string = "./Assets/Characters/Character_1/Expressions/Happy.png"
	current_character = "Character_4"
	texture = load(texture_string)
	pass # Replace with function body.
