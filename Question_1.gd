extends RichTextLabel


var final_text 
var text_dict = {}



func _ready():
	pass 




func _on_Next_Button_pressed():
	text = text_dict['Question_1']['question']
	pass 


func _on_Final_Screen_Text_file_loaded(dict):
	text_dict = dict
	pass 
