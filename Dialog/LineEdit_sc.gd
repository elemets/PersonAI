extends LineEdit

signal user_text_input(text)


func _ready():
	release_focus()
	pass


func _on_RichTextLabel_conversation_finished():
	grab_focus()
	pass # Replace with function body.


func _on_LineEdit_text_entered(new_text):
	text = ''
	release_focus()
	pass # Replace with function body.
