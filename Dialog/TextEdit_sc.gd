extends TextEdit


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var text_to_display 
var output = []
onready var file = 'res://output.txt'
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


func load_file(file):
	var f = File.new()
	f.open(file, File.READ)
	var index = 1
	while not f.eof_reached():
		text_to_display = f.get_line()
	f.close()
	return

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
