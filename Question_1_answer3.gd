extends LineEdit



var text_dict = {}
var required_answer 
signal question_3_correct(q_3_bool)

# Called when the node enters th
func _ready():
	self.hide()
	if text_dict.has("Question_3"):
		required_answer = text_dict['Question_3']['correct-answer']
		required_answer = required_answer.to_lower()
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_Next_Button_pressed():
	if text_dict.has("Question_3"):
		self.show()
	pass # Replace with function body.


func _on_Final_Screen_Text_file_loaded(dict):
	text_dict = dict
	pass # Replace with function body.


func _on_Final_Button_pressed():
	text = text.to_lower()
	if text_dict.has("Question_3"):
		if text.similarity(required_answer) > 0.8:
			emit_signal("question_3_correct", true)
		else:
			emit_signal("question_3_correct", false)
	pass # Replace with function body.
