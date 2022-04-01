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


func _on_Character_3_text_dict(dict):
	var current_size = texture.get_size()
	var desired_size = ''
	if dict['Characters'].has("Character_3"):
		texture = load("./Assets/Characters/Character_3/Character_3_Sprite.png")
		hframes = dict['Character_hframes']['Character_3_hframes']
		vframes = dict['Character_vframes']['Character_3_vframes']
		desired_size = Vector2(32 * hframes, 32 * vframes)
	else:
		desired_size = Vector2(32 * hframes, 32 * vframes)
	scale = desired_size / current_size
	pass # Replace with function body.

