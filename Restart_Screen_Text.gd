extends RichTextLabel

var final_text 
var text_dict = {}

func _ready():
	var file = File.new()
	file.open("./Assets/InfoJSONs/final_screen.json", file.READ)
	var text_returned = file.get_as_text()
	text_dict = JSON.parse(text_returned).result
	file.close()




func _on_WinOrLose_win_or_lose(winorlose):
	if winorlose == 'win':
		text = text_dict['winning_screen_text']
	else:
		text = text_dict['losing_screen_text']
	pass # Replace with function body.
