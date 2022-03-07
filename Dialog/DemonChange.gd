extends Sprite


# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_RichTextLabel_mood(emotion):
	if emotion == 'pos':
		texture = load("res://Characters/Demon/Expressions/Happy.png")
	elif emotion == 'neg':
		texture = load("res://Characters/Demon/Expressions/Sad.png")
	else:
		texture = load("res://Characters/Demon/Expressions/Neutral.png")
	pass # Replace with function body.
