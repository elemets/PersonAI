extends RichTextLabel

# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var text_to_display 
var output = []
var pid
var file = 'output.txt'
# Called when the node enters the scene tree for the first time.
func _ready():
	$OSAsyncExecute.execute("./fast_speech_cli/fast_speech_cli.exe", ["artorius"], "greeting")
	pass # Replace with function body.

func load_file(file):
	var f = File.new()
	f.open(file, File.READ)
	var text = f.get_as_text()
	f.close()
	return text

func _on_OSAsyncExecute_command_finished(path, arguments, output, exit_code, identifier):
	print("finished", identifier, " ", "output")
	text = load_file(file)

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
