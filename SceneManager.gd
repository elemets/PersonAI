extends Node2D

const DialogScene = preload("res://Dialog/Dialog.tscn")


func _on_TransitionScreen_transition():
	$CurrentScene.get_child(0).queue_free()
	$CurrentScene.hide()
	print("Changed to Dialog Screen")


func _on_Demon_conversation(demon_name):
	$TransitionScreen.transition()



func _on_Demon2_conversation(demon_name):
	$TransitionScreen.transition()
	pass # Replace with function body.
