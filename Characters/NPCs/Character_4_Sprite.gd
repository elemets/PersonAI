extends Sprite




func _ready():
	pass 


func _on_Character_4_text_dict(text_dict):
	texture = load("./Assets/Characters/Character_4/Character_4_Sprite.png")
	if text_dict['Characters'].has("Character_4"):
		hframes = text_dict['Character_hframes']['Character_4_hframes']
		vframes = text_dict['Character_vframes']['Character_4_vframes']
	var current_size = texture.get_size()
	var desired_size = Vector2(64, 64)
	scale = desired_size / current_size
	pass # Replace with function body.
