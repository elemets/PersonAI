extends RichTextLabel



var final_text 
var text_dict = {}

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


func _on_Next_Button_pressed():
	if text_dict.has('Question_4'):
		text = text_dict['Question_4']['question']
	pass # Replace with function body.


func _on_Final_Screen_Text_file_loaded(dict):
	text_dict = dict
	pass # Replace with function body.
