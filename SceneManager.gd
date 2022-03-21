extends Node2D

onready var dialogScene = $Dialog
onready var currentScene = $CurrentScene
onready var finalScreen = $FinalScreen
var final_screen_btn = false
var exit_screen_btn = false
signal exit_screen

func _on_TransitionScreen_transition():
	var children = self.get_children()

	if children.has(finalScreen) and exit_screen_btn:
		remove_child(finalScreen)
		emit_signal("exit_screen")
	elif children.has(currentScene) and final_screen_btn:
		remove_child(currentScene)
		remove_child(dialogScene)
		print(final_screen_btn)
	elif children.has(currentScene) and final_screen_btn == false:
		remove_child(currentScene)
		add_child(dialogScene)
	else:
		remove_child(dialogScene)
		add_child(currentScene)
	
	print("Changed to Dialog Screen")


func _on_Demon_conversation(demon_name):
	$TransitionScreen.transition()



func _on_Demon2_conversation(demon_name):
	$TransitionScreen.transition()
	pass # Replace with function body.



func _on_RichTextLabel_exit_dialog():
	$TransitionScreen.transition()
	pass # Replace with function body.



func _on_TextureButton_pressed():
	final_screen_btn = true
	$TransitionScreen.transition()
	pass # Replace with function body.


func _on_Final_Button_pressed():
	exit_screen_btn = true 
	$TransitionScreen.transition()
	pass # Replace with function body.
