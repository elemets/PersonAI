extends Sprite


# Declare member variables here. Examples:
# var a = 2
# var b = "text"



# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_Character_1_text_dict(dict):
	var current_size = texture.get_size()
	var desired_size = ''
	if dict['Characters'].has("Character_1"):
		texture = load("./Assets/Characters/Character_1/Character_1_Sprite.png")
		hframes = dict['Character_hframes']['Character_1_hframes']
		vframes = dict['Character_vframes']['Character_1_vframes']
		desired_size = Vector2(32 * hframes, 32 * vframes)
	else:
		desired_size = Vector2(32 * hframes, 32 * vframes)
	scale = desired_size / current_size
	pass # Replace with function body.
