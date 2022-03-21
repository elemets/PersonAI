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
var chatLimit = 145
var demon_name
var payload_received
signal exit_dialog
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


	
func _process(delta):
	_showCharacter()
	if Input.is_key_pressed(KEY_E):
		text = ''
		emit_signal("conversation_finished")
	elif Input.is_key_pressed(KEY_ESCAPE):
		emit_signal("exit_dialog")
	
	
	

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
	payload_received = true
	text = payload['Content']
	emit_signal("mood", payload['Emotion'])
	var prob_score = payload['prob_score']
	if prob_score:
		if prob_score > 0.8:
			text = "The demon says with conviction: " + text 
			emit_signal("mood", "pos")
		elif prob_score > 0.5:
			text = "The demon says with a glint of uncertainty in their eyes: " + text
			emit_signal("mood", "neutral")
		elif prob_score > 0.3:
			text = "Hmm I'm really not sure about this but, " + text
			emit_signal("mood", "neutral")
		elif prob_score > 0.2:
			text = "The demon looks confused and averts their eyes, ignoring your question."
			emit_signal("mood", "neg")

	pass # Replace with function body.
