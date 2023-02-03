extends Node2D

onready var dialogScene = $Dialog
onready var currentScene = $CurrentScene
onready var finalScreen = $FinalScreen
onready var introScreen = $IntroScreen
onready var restartScreen = $RestartMenu
var final_screen_btn = false
var menu_button = false
var exit_screen_btn = false
var retry_btn = false
signal exit_screen


func _on_TransitionScreen_transition():
	var children = self.get_children()

	if menu_button and children.has(introScreen):
		remove_child(introScreen)
	elif children.has(finalScreen) and exit_screen_btn:
		remove_child(finalScreen)
		add_child(restartScreen)
		emit_signal("exit_screen")
	elif children.has(currentScene) and final_screen_btn:
		remove_child(currentScene)
		remove_child(dialogScene)
		add_child(finalScreen)
	elif children.has(currentScene) and final_screen_btn == false:
		remove_child(currentScene)
		add_child(dialogScene)
	elif children.has(restartScreen) and retry_btn:
		remove_child(restartScreen)
		add_child(dialogScene)
		add_child(currentScene) 
		retry_btn = false
		exit_screen_btn = false
		menu_button = false
		final_screen_btn = false
	else:
		remove_child(dialogScene)
		add_child(currentScene)
	
	print("Changed to Dialog Screen")


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



func _on_Character_2_conversation(demon_name):
	$TransitionScreen.transition()



func _on_Character_1_conversation(demon_name):
	$TransitionScreen.transition()


func _on_StartButton_pressed():
	menu_button = true 
	$TransitionScreen.transition()
	pass # Replace with function body.


func _on_Character_3_conversation(demon_name):
	$TransitionScreen.transition()
	pass # Replace with function body.


func _on_Character_4_conversation(demon_name):
	$TransitionScreen.transition()
	pass # Replace with function body.
	


func _on_RetryButton_pressed():
	retry_btn = true
	$TransitionScreen.transition()
	pass # Replace with function body.
