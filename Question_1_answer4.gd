extends LineEdit


var final_text 
var text_dict = {}
var required_answer 
signal question_4_correct(q_4_bool)


func _ready():
	self.hide()
	if text_dict.has("Question_4"):
		required_answer = text_dict['Question_4']['correct-answer']
		required_answer = required_answer.to_lower()
	pass # Replace with function body.




func _on_Next_Button_pressed():
	if text_dict.has("Question_4"):
		self.show()
	pass


func _on_Final_Screen_Text_file_loaded(dict):
	text_dict = dict
	pass 


func _on_Final_Button_pressed():
	text = text.to_lower()
	var q_4_wrong_answer = text
	if text_dict.has("Question_4"):
		if text.similarity(required_answer) > 0.8:
			emit_signal("question_4_correct", true, null)
		else:
			emit_signal("question_4_correct", false, q_4_wrong_answer)
	pass # Replace with function body.
