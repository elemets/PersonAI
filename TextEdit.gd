extends TextEdit

signal user_text_input(text)


func _ready():
	pass


func _on_RichTextLabel_conversation_finished():
	grab_focus()
	pass 



func _on_TextEdit_breakpoint_toggled(row):
	emit_signal("user_text_input", row)
	text = ''
	pass # Replace with function body.
