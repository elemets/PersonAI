extends Node2D

const DialogScene = preload("res://Dialog/Dialog.tscn")


func _on_TransitionScreen_transition():
	$CurrentScene.get_child(0).queue_free()
	$CurrentScene.add_child(DialogScene.instance())
	print("Changed to Dialog Screen")


func _on_Demon_conversation():
	$TransitionScreen.transition()

