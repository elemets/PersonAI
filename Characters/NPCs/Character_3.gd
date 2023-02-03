extends KinematicBody2D

export var ACCELERATION = 600
export var MAX_SPEED = 70
export var FRICTION = 200
var waiting_for_payload = false
var NAME


enum {
	IDLE,
	IN_CONVERSATION,
	WANDER
}

enum {
	LEFT,
	RIGHT
}




const TOLERANCE = 4.0

onready var PlayerDetectionZone_3 = $PlayerDetectionZone_3


var rng = RandomNumberGenerator.new()
signal conversation(demon_name)
signal name(NAME)
var anim
onready var animation_player = $Characer_3_Animation
var text_dict = {}

onready var timer = get_node("Timer")
func _ready():
	start_position = global_position
	var file = File.new()
	file.open("./Assets/Character_Info/character_names.json", file.READ)
	var text_returned = file.get_as_text()
	text_dict = JSON.parse(text_returned).result
	file.close()
	print(text_dict)
	if text_dict['Characters'].has("Characer_3"):
		NAME = text_dict['Characters']['Characer_3']
		if text_dict['Character_hframes']['Characer_3_hframes'] > 1 and text_dict['Character_vframes']['Characer_3_vframes'] > 1:
			anim = true 
		emit_signal("name", NAME)
		print("Emitting signal", NAME)
	timer.set_wait_time(5)
	timer.start()


func TimerTimeout():
	pass
	

enum AIState {
	IDLE,
	WANDER,
}

enum SquareDirection {
	LEFT,
	RIGHT,
}

const ZERO = Vector2(0, 0)

var state = AIState.WANDER
var square_next = SquareDirection.LEFT
var velocity = Vector2.ZERO
var target_position = Vector2.ZERO
var start_position = Vector2.ZERO



func _physics_process(delta):
	see_player()
	move_towards_target(delta)
	velocity = move_and_slide(velocity)

func see_player():
	if PlayerDetectionZone_3.can_see_player():
		idle()
	else:
		wander()

func idle():
	state = AIState.IDLE
	velocity = velocity.move_toward(ZERO, FRICTION)
	var player = PlayerDetectionZone_3.player
	if player != null and Input.is_key_pressed(KEY_E):
		emit_signal("conversation", NAME)

func wander():
	state = AIState.WANDER
	var direction = (update_target_position() - global_position).normalized()
	velocity = velocity.move_toward(direction * MAX_SPEED, ACCELERATION)

func move_towards_target(delta):
	var direction = (update_target_position() - global_position).normalized()
	if (target_position - global_position).length() > TOLERANCE:
		velocity = velocity.move_toward(direction * MAX_SPEED, ACCELERATION * delta)
	else:
		square_next = SquareDirection.LEFT if square_next == SquareDirection.RIGHT else SquareDirection.RIGHT

func update_target_position():
	if square_next == SquareDirection.LEFT:
		target_position = Vector2(start_position.x - 100, start_position.y)
		if anim:
			animation_player.play("run_left")
	else:
		target_position = Vector2(start_position.x + 100, start_position.y)
		if anim:
			animation_player.play("run_right")
	return target_position
