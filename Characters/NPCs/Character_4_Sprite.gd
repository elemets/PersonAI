extends Sprite




func _ready():
	pass 


func _on_Character_4_text_dict(dict):
	var current_size = texture.get_size()
	var desired_size = ''
	if dict['Characters'].has("Character_4"):
		texture = load("./Assets/Characters/Character_4/Character_4_Sprite.png")
		hframes = dict['Character_hframes']['Character_4_hframes']
		vframes = dict['Character_vframes']['Character_4_vframes']
		desired_size = Vector2(32 * hframes, 32 * vframes)
	else:
		desired_size = Vector2(32 * hframes, 32 * vframes)
	scale = desired_size / current_size
	pass # Replace with function body.
