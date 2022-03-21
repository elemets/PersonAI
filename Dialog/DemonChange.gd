extends Sprite


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var demon_name = 'Magdela'
var texture_string
# Called when the node enters the scene tree for the first time.
func _ready():
	texture_string = "res://Characters/Demon/"+ demon_name +"/Expressions/Happy.png"
	texture = load(texture_string)
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_RichTextLabel_mood(emotion):
	print("emotion received")
	print(emotion)
	if emotion == 'pos':
		texture_string = "res://Characters/Demon/"+ demon_name +"/Expressions/Happy.png"
		texture = load(texture_string)
	elif emotion == 'neg':
		texture_string = "res://Characters/Demon/"+ demon_name +"/Expressions/Sad.png"
		texture = load(texture_string)
	else:
		texture_string = "res://Characters/Demon/"+ demon_name +"/Expressions/Neutral.png"
		texture = load(texture_string)
	pass # Replace with function body.





func _on_Demon2_conversation(demon_name):
	demon_name = demon_name
	texture_string = "res://Characters/Demon/"+ demon_name +"/Expressions/Happy.png"
	texture = load(texture_string)
	pass # Replace with function body.


func _on_Demon_conversation(demon_name):
	demon_name = demon_name
	texture_string = "res://Characters/Demon/"+ demon_name +"/Expressions/Happy.png"
	texture = load(texture_string)
	pass # Replace with function body.
