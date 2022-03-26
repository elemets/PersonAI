extends Sprite


# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_Character_3_text_dict(text_dict):
	if text_dict['Characters'].has("Character_3"):
		texture = load("./Assets/Characters/Character_3/Character_3_Sprite.png")
		hframes = text_dict['Character_hframes']['Character_3_hframes']
		vframes = text_dict['Character_vframes']['Character_3_vframes']
	frame = 0
	var current_size = texture.get_size()
	var desired_size = Vector2(64, 64)
	scale = desired_size / current_size
	print("Here")
	pass # Replace with function body.

