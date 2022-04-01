extends Node2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	$OSAsyncExecute.execute("./execute_bash.bat",[], "Start Server")
	pass # Replace with function body.
	
func _on_OSAsyncExecute_command_finished(path, arguments, output, exit_code, identifier):
	print("finished ", identifier, " ", output)


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
