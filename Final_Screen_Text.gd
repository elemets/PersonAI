extends RichTextLabel


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var final_text 
var text_dict = {}
signal file_loaded(dict)

# Called when the node enters the scene tree for the first time.
func _ready():
	var file = File.new()
	file.open("./Assets/InfoJSONs/final_screen.json", file.READ)
	var text_returned = file.get_as_text()
	text_dict = JSON.parse(text_returned).result
	file.close()
	text = text_dict['final_screen_text']
	emit_signal("file_loaded", text_dict)
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_Next_Button_pressed():
	text = ''
	pass # Replace with function body.
