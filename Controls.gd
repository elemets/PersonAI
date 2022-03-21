extends RichTextLabel


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var text_dict = {}

# Called when the node enters the scene tree for the first time.
func _ready():
	var file = File.new()
	file.open("./Assets/InfoJSONs/information_screen.json", file.READ)
	var text_returned = file.get_as_text()
	text_dict = JSON.parse(text_returned).result
	file.close()
	var controls = text_dict['Controls']
	for c in controls:
		text += c + "\n"
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
