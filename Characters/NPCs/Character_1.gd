extends KinematicBody2D

export var ACCELERATION = 600
export var MAX_SPEED = 70
export var FRICTION = 200
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

var square_next = RIGHT


const TOLERANCE = 4.0
var velocity = Vector2.ZERO
var state = WANDER
onready var playerDetectionZone = $PlayerDetectionZone
onready var start_position = global_position
onready var target_position = global_position
var rng = RandomNumberGenerator.new()
signal conversation(demon_name)
signal name(NAME)
onready var animation_player = $AnimationPlayer
var text_dict = {}

onready var timer = get_node("Timer")
func _ready():
	var file = File.new()
	file.open("./Assets/Character_Info/character_names.json", file.READ)
	var text_returned = file.get_as_text()
	text_dict = JSON.parse(text_returned).result
	file.close()
	NAME = text_dict['Character_1']
	emit_signal("name", NAME)
	print("Emitting signal", NAME)
	timer.set_wait_time(5)
	timer.start()


func TimerTimeout():
	pass

func _physics_process(delta):
	see_player()
	match state:
		IDLE:
			var player = playerDetectionZone.player
			if player != null and Input.is_key_pressed(KEY_E):
				print("emitting conversation")
				emit_signal("conversation", NAME)
			elif player != null:
				velocity = velocity.move_toward(Vector2.ZERO, FRICTION *delta)
		WANDER:
			var player = playerDetectionZone.player
			var point = update_target_position()
			var direction = (point - global_position).normalized()
			print(direction)
			if player ==  null:
				velocity = velocity.move_toward(direction * MAX_SPEED, ACCELERATION * delta)

	velocity = move_and_slide(velocity)

func see_player():
	if playerDetectionZone.can_see_player():
		state = IDLE
	else:
		state = WANDER
		
		
func update_target_position():
	var target_vector = Vector2.ZERO

	match square_next:
		LEFT:
			target_vector = Vector2(start_position.x - 100, start_position.y)
			animation_player.play("run_left")
			if is_at_target_position():
				square_next = RIGHT
			target_position = target_vector
		RIGHT:
			target_vector = Vector2(start_position.x + 100, start_position.y)
			animation_player.play("run_right")
			if is_at_target_position():
				square_next = LEFT
			target_position = target_vector
	return target_position

func is_at_target_position():
	return (target_position - global_position).length() < TOLERANCE

