extends RichTextLabel

var final_text 
var text_dict = {}

func _ready():
	var file = File.new()
	file.open("./Assets/InfoJSONs/final_screen.json", file.READ)
	var text_returned = file.get_as_text()
	text_dict = JSON.parse(text_returned).result
	file.close()




func _on_WinOrLose_win_or_lose(winorlose, demon_who_lied, the_answer_they_gave):
	if winorlose == 'win':
		text = text_dict['winning_screen_text']
	elif demon_who_lied:
		var text_to_load_correct_demon = 'losing_screen_text_' + demon_who_lied
		text = the_answer_they_gave + "??? " + text_dict[text_to_load_correct_demon]
	else:
		text = text_dict['losing_screen_text']
		## function is needed here to display the demon which
		## has lied to you maybe set it up so they give a clue about what lie they told
		## e.g. if the lie was about the basement
	pass # Replace with function body.
