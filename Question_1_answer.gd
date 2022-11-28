extends LineEdit


var text_dict = {}
var required_answer
signal question_1_correct(q_1_bool)
# Called when the node enters the scene tree for the first time.
func _ready():
	self.hide()
	if text_dict.has("Question_1"):
		required_answer = text_dict['Question_1']['correct-answer']
		required_answer = required_answer.to_lower()



func _on_Next_Button_pressed():
	self.show()



func _on_Final_Screen_Text_file_loaded(dict):
	text_dict = dict



func _on_Final_Button_pressed():
	text = text.to_lower()
	var q_1_wrong_answer = text
	if text.similarity(required_answer) > 0.8:
		emit_signal("question_1_correct", true, null)
	else:
		emit_signal("question_1_correct", false, q_1_wrong_answer)

