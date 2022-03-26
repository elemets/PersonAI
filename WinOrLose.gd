extends RichTextLabel


var truth_list = []
signal win_or_lose(winorlose)

func _ready():
	pass

func _win_checker():
	if false in truth_list:
		text = "YOU LOSE"
		emit_signal("win_or_lose", "lose")
	else:
		text = "YOU WIN"
		emit_signal("win_or_lose", "win")
		

func _on_Question_1_answer4_question_4_correct(q_4_bool):
	truth_list.append(q_4_bool)



func _on_Question_1_answer2_question_2_correct(q_2_bool):
	truth_list.append(q_2_bool)



func _on_Question_1_answer3_question_3_correct(q_3_bool):
	truth_list.append(q_3_bool)



func _on_Question_1_answer_question_1_correct(q_1_bool):
	truth_list.append(q_1_bool)



func _on_SceneManager_exit_screen():
	_win_checker()
	print("Win checking")
