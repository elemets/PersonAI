extends Node2D

export var SOCKET_URL = "ws://127.0.0.1:1234"

var demon_name
var command
var content
signal payload_received
var _client = WebSocketClient.new()
var waiting_for_payload = false 

func _ready():
	_client.connect("connection_closed", self, "_on_connection_closed")
	_client.connect("connection_error", self, "_on_connection_closed")
	_client.connect("connection_established", self, "_on_connected")
	_client.connect("data_received", self, "_on_data")
	
	var err = _client.connect_to_url(SOCKET_URL)
	
	print(err)
	
	if err != OK:
		print("Unable to connect")
		set_process(false)
	

func _process(delta):
	_client.poll()
	
func _on_connection_closed(was_clean = false):
	print("Closed, clean: ", was_clean)
	set_process(false)
	
func _on_connected(proto = ""):
	print("Connected with protocol: ", proto)
	print("Sending initialise to the demon")
	_send(demon_name, 'init')
	
func _on_data():
	var payload = JSON.parse(_client.get_peer(1).get_packet().get_string_from_utf8()).result
	print(payload)
	waiting_for_payload = false
	if payload['Type'] == 'greet' or payload['Type'] == 'response':
		emit_signal("payload_received", payload)

func _send(demon_name, command, content=''):
	_client.get_peer(1).put_packet(JSON.print({"Name": demon_name, "Command": command, "Content": content}).to_utf8())


func _on_Demon_name(NAME):
	demon_name = NAME
	command = 'init'
	pass # Replace with function body.


func _on_Demon_conversation(demon_name):
	command = 'greet'
	demon_name = demon_name
	if waiting_for_payload == false:
		_send(demon_name, command)
		waiting_for_payload = true
	pass # Replace with function body.


func _on_RichTextLabel_Player_Response(message):
	if waiting_for_payload == false:
		_send(demon_name, "response", message)
		waiting_for_payload = true
	pass # Replace with function body.


func _on_Demon2_conversation(demon_name):
	command = 'greet'
	demon_name = demon_name
	if waiting_for_payload == false:
		_send(demon_name, command)
		waiting_for_payload = true
	pass # Replace with function body.


func _on_Demon2_name(NAME):
	demon_name = NAME
	command = 'init'
	pass # Replace with function body.
