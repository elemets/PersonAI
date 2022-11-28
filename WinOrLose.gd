extends RichTextLabel


var truth_list = []
signal win_or_lose(winorlose)
var question_dict = {}
var char_dict = {}
var lied_on_q_4 = false 
var lied_on_q_3 = false
var lied_on_q_2 = false
var lied_on_q_1 = false
var demon_who_lied 
var wrong_answer

func _ready():
	pass

func _load_char_dict(char_name):
	var file = File.new()
	file.open("./Assets/Characters/"+ char_name + ".json", file.READ)
	var text_returned = file.get_as_text()
	char_dict = JSON.parse(text_returned).result
	file.close()
	var player_rating = float(char_dict['Player_Rating'])
	var demon_lied = false
	if player_rating < 10:
		demon_lied = true
	return demon_lied
	
	
	


func _win_checker():
	
	if lied_on_q_1 == true or lied_on_q_2 == true or lied_on_q_3 == true or lied_on_q_4 == true:
		emit_signal("win_or_lose", "lose", demon_who_lied, wrong_answer)
	elif false in truth_list:
		emit_signal("win_or_lose", "lose", demon_who_lied, null)
	else:
		text = "YOU WIN"
		emit_signal("win_or_lose", "win", null, null)
		

func _on_Question_1_answer4_question_4_correct(q_4_bool, q_4_wrong_answer):
	var char_with_kno_of_q_4 = question_dict['Question_4']['character-with-knowledge']
	
	var did_demon_lie = _load_char_dict(char_with_kno_of_q_4)
	
	## this means that the answer given was incorrect and that the demon was
	## not in the final stages of it's context this means that we can say the NPC has lied to
	## the player
	if did_demon_lie == true and q_4_bool == false:
		lied_on_q_4 = true 
		demon_who_lied = char_with_kno_of_q_4
		wrong_answer = q_4_wrong_answer
	
	
	
	truth_list.append(q_4_bool)



func _on_Question_1_answer2_question_2_correct(q_2_bool, q_2_wrong_answer):
	## checking whether the question is answerable based off which context the character was in
	## first find the character
	var char_with_kno_of_q_2 = question_dict['Question_2']['character-with-knowledge']
	
	var did_demon_lie = _load_char_dict(char_with_kno_of_q_2)
	
	if did_demon_lie == true and q_2_bool == false:
		lied_on_q_2 = true 
		demon_who_lied = char_with_kno_of_q_2
		wrong_answer = q_2_wrong_answer
	
	truth_list.append(q_2_bool)



func _on_Question_1_answer3_question_3_correct(q_3_bool, q_3_wrong_answer):
	var char_with_kno_of_q_3 = question_dict['Question_3']['character-with-knowledge']
	
	var did_demon_lie = _load_char_dict(char_with_kno_of_q_3)

	if did_demon_lie == true and q_3_bool == false:
		lied_on_q_3 = true 
		demon_who_lied = char_with_kno_of_q_3
		wrong_answer = q_3_wrong_answer
	
	truth_list.append(q_3_bool)



func _on_Question_1_answer_question_1_correct(q_1_bool, q_1_wrong_answer):
	var char_with_kno_of_q_1 = question_dict['Question_1']['character-with-knowledge']
	
	var did_demon_lie = _load_char_dict(char_with_kno_of_q_1)

	if did_demon_lie == true and q_1_bool == false:
		lied_on_q_1 = true 
		demon_who_lied = char_with_kno_of_q_1
		wrong_answer = q_1_wrong_answer
		
	truth_list.append(q_1_bool)



func _on_SceneManager_exit_screen():
	_win_checker()
	print("Win checking")


func _on_Final_Screen_Text_file_loaded(dict):
	question_dict = dict
	pass # Replace with function body.
