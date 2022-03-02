extends Area2D

var player = null


func can_see_player():
	return player != null

func _on_PlayerDetectionZone_body_entered(body):
	player = body
	pass # Replace with function body.


func _on_PlayerDetectionZone_body_exited(body):
	player = null
	pass # Replace with function body.
