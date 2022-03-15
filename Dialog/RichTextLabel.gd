extends RichTextLabel

# Declare member variables here. Examples:
# var a = 2
# var b = "text"

signal conversation_finished
var text_to_display 
var output = []
var result_dict = {}
var pid
signal mood(emotion)
signal Player_Response(message)
var drawTextSpeed = 0
var chatLimit = 56
var demon_name
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


func _on_OSAsyncExecute_command_finished(path, arguments, output, exit_code, identifier):
	var result_json = JSON.parse(output)
	var result = {}
	var data = result_json.result
	text = data['Output']
	emit_signal("mood", data['Type'])
	
func _process(delta):
	_showCharacter()
	if Input.is_key_pressed(KEY_E):
		text = ''
		emit_signal("conversation_finished")
	
	

func _showCharacter():
	if !text:
		pass
	elif drawTextSpeed < chatLimit:
		drawTextSpeed += 1
		self.visible_characters = drawTextSpeed


func _on_LineEdit_text_entered(new_text):
	if new_text != '':
		emit_signal("Player_Response", new_text)
	pass # Replace with function body.


func _on_Socket_payload_received(payload):
	text = payload['Content']
	pass # Replace with function body.