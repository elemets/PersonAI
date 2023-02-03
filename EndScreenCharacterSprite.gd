extends Sprite

var character_names
var char_1_name
var char_2_name
var char_3_name
var char_4_name
var char_num
# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	var file = File.new()
	file.open("./Assets/Character_Info/character_names.json", file.READ)
	var text_returned = file.get_as_text()
	character_names = JSON.parse(text_returned).result
	file.close()
	char_1_name = character_names['Characters']['Character_1']
	
	if character_names['Characters'].has("Character_2"):
		char_2_name = character_names['Characters']['Character_2']
	
	if character_names['Characters'].has("Character_3"):
		char_3_name = character_names['Characters']['Character_3']
	
	if character_names['Characters'].has("Character_4"):
		char_4_name = character_names['Characters']['Character_4']

		
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_WinOrLose_win_or_lose(winorlose, demon_who_lied, wrong_answer):
	
	if char_1_name == demon_who_lied:
		char_num = 'Character_1'
	if char_2_name == demon_who_lied:
		char_num = 'Character_2'
	if char_3_name == demon_who_lied:
		char_num = 'Character_3'
	if char_4_name == demon_who_lied:
		char_num = 'Character_4'
	
	

	var texture_string = "./Assets/Characters/"+  char_num + "/Expressions/Happy.png"
	texture = load(texture_string)
	pass # Replace with function body.
