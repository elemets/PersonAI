extends Node2D

export var SOCKET_URL = "ws://127.0.0.1:1234"

var demon_name
var demon_name_2
var demon_name_3
var demon_name_4
signal waiting_for_payload
var command
var content
signal payload_received
var _client = WebSocketClient.new()
var waiting_for_payload = false 
var character_dict = {}
var current_convo
signal game_loaded

func _ready():
	_load_character_dict()
	_client.connect("connection_closed", self, "_on_connection_closed")
	_client.connect("connection_error", self, "_on_connection_closed")
	_client.connect("connection_established", self, "_on_connected")
	_client.connect("data_received", self, "_on_data")
	
	var err = _client.connect_to_url(SOCKET_URL)
	if err != OK:
		print("Unable to connect")
		set_process(false)
	

func _load_character_dict():
	var file = File.new()
	file.open("./Assets/Character_Info/character_names.json", file.READ)
	var text_returned = file.get_as_text()
	character_dict = JSON.parse(text_returned).result
	file.close()
	

func _process(delta):
	_client.poll()
	
func _on_connection_closed(was_clean = false):
	print("Closed, clean: ", was_clean)
	set_process(false)
	
func _on_connected(proto = ""):
	print("Connected with protocol: ", proto)
	print("Sending initialise to the demon")
	_send("Character_1", 'init')

	if character_dict['Characters'].has("Character_2"):
		_send("Character_2", 'init')
	if character_dict['Characters'].has("Character_3"):
		_send("Character_3", 'init')
	if character_dict['Characters'].has("Character_4"):
		_send("Character_4", 'init')
	
func _on_data():
	var payload = JSON.parse(_client.get_peer(1).get_packet().get_string_from_utf8()).result
	waiting_for_payload = false
	if payload['Type'] == 'initialised':
		emit_signal("game_loaded")
		print("loaded")
	if payload['Type'] == 'greet' or payload['Type'] == 'response':
		emit_signal("payload_received", payload)
	

func _send(character_num, command, content=''):
	print(character_num)
	_client.get_peer(1).put_packet(JSON.print({"Name": character_num, "Command": command, "Content": content}).to_utf8())

func _on_RichTextLabel_Player_Response(message):
	if waiting_for_payload == false:
		waiting_for_payload = true
		_send(current_convo, "response", message)
	pass # Replace with function body.


func _on_Character_2_conversation(demon_name):
	command = 'greet'
	demon_name_2 = "Character_2"
	print("character 2 conversation active")
	print("sending")
	print(demon_name_2)	
	if waiting_for_payload == false:
		emit_signal("Waiting for payload")
		waiting_for_payload = true
		_send("Character_2", command)
		current_convo = demon_name_2
	pass # Replace with function body.


func _on_Character_2_name(NAME):
	demon_name = "Character_2"
	command = 'init'
	pass 


func _on_Character_1_name(NAME):
	demon_name = 'Character_1'
	command = 'init'
	print("Character one triggers")
	pass 


func _on_Character_1_conversation(demon_name):
	command = 'greet'
	demon_name = "Character_1"
	print("character 1 conversation active")
	print("sending")
	print(demon_name)
	if waiting_for_payload == false:
		emit_signal("Waiting for payload")
		waiting_for_payload = true
		_send("Character_1", command)
		current_convo = demon_name
	pass 


func _on_Final_Screen_Text_file_loaded(dict):
	character_dict = dict
	pass # Replace with function body.


func _on_Character_3_conversation(demon_name):
		
	command = 'greet'
	if waiting_for_payload == false:
		emit_signal("Waiting for payload")
		waiting_for_payload = true
		demon_name_3 = "Character_3"
		_send("Character_3", command)
		print("Sending")
		current_convo = demon_name_3
	pass # Replace with function body.


func _on_Character_3_name(NAME):
	demon_name = 'Character_3'
	command = 'init'
	pass # Replace with function body.


func _on_Character_4_name(NAME):
	demon_name = 'Character_4'
	command = 'init'
	pass # Replace with function body.


func _on_Character_4_conversation(demon_name):
	if waiting_for_payload == false:
		emit_signal("Waiting for payload")
		waiting_for_payload = true
		command = 'greet'
		demon_name_4 = "Character_4"
		_send("Character_4", command)
		current_convo = demon_name_4
	pass # Replace with function body.
