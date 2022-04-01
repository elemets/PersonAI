extends Sprite


func _ready():
	pass 


func _on_Character_2_text_dict(dict):
	var current_size = texture.get_size()
	var desired_size = ''
	if dict['Characters'].has("Character_2"):
		texture = load("./Assets/Characters/Character_2/Character_2_Sprite.png")
		hframes = dict['Character_hframes']['Character_2_hframes']
		vframes = dict['Character_vframes']['Character_2_vframes']
		desired_size = Vector2(32 * hframes, 32 * vframes)
	else:
		desired_size = Vector2(32 * hframes, 32 * vframes)
	scale = desired_size / current_size
	pass 
