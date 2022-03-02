extends CanvasLayer


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
signal transition

 
	
func transition():
	$AnimationPlayer.play("fade_to_black")


func _on_AnimationPlayer_animation_finished(anim_name):
	if anim_name == "fade_to_black":
		print("Emit signal transition")
		emit_signal("transition")
		$AnimationPlayer.play("fade_to_normal")
	if anim_name == "fade_to_normal":
		print("Finished transitioning")
