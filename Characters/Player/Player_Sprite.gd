extends Sprite


# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	texture = load("./Assets/Player.png")
	var size = texture.get_size()
	var sizeTo = Vector2(32, 32)
	var s = sizeTo/ size
	scale = s





# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
