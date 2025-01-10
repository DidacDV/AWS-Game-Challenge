extends Node
class_name WebSocketClient 

var socket = WebSocketPeer.new()
var last_state = WebSocketPeer.STATE_CLOSED
var json_parser = JSON.new()
var lobbyId = ""

signal connected_to_server()
signal connection_closed()
signal message_received(message: Variant)
signal position_update(playerId: String, newPosition: Vector2)


func _ready():
	message_received.connect(_on_message_received)

func poll() -> void:
	if socket.get_ready_state() != socket.STATE_CLOSED:
		socket.poll()
	
	var state = socket.get_ready_state()
	if last_state != state:
		last_state = state
		if state == socket.STATE_OPEN:
			connected_to_server.emit()
		elif state == socket.STATE_CLOSED:
			connection_closed.emit()
	while socket.get_ready_state() == socket.STATE_OPEN and socket.get_available_packet_count():
		print("message received!")
		message_received.emit(get_message())
		
	
func send(message) -> int:
	if typeof(message) == TYPE_STRING:
		return socket.send_text(message)  
	elif typeof(message) == TYPE_DICTIONARY or typeof(message) == TYPE_ARRAY:
		return socket.send_text(JSON.stringify(message)) 
	else:
		return socket.send_text(str(message)) 
		
func get_message() -> Variant:
	if socket.get_available_packet_count() < 1:
		return null
		
	var packet = socket.get_packet()
	if socket.was_string_packet():
		return packet.get_string_from_utf8()
	
	return bytes_to_var(packet)

func connect_to_url(url) -> int:
	var error = socket.connect_to_url(url)
	print("attempting to connect to %s" % [url])
	if error != OK:
		return error
		
	last_state = socket.get_ready_state()
	return OK

func close(code := 1000, reason := "") -> void:
	print("closing....")
	socket.close(code, reason)
	last_state = socket.get_ready_state()

func get_socket() -> WebSocketPeer:
	return socket
	
func _process(delta):
	poll()
	
func setLobbyId(newId):
	lobbyId = newId

func create_lobby(lobby_id: String) -> void:
	var message = {
		"action": "create_lobby",  # Changed to match Lambda
		"lobbyId": lobby_id
	}
	send(message)

func join_lobby(lobby_id: String) -> void:
	var message = {
		"action": "join_lobby",  # Changed to match Lambda
		"lobbyId": lobby_id
	}
	send(message)

func send_lobby_message(message_content: String) -> void:
	var message = {
		"action": "send_message",  # Changed to match Lambda
		"lobbyId": lobbyId,
		"message": message_content  # Changed from payload to message
	}
	send(message)

func send_position(lobby_id: String, position: Vector2) -> void:
	var message = {
		"action": "update_position",
		"lobbyId": lobby_id,
		"position": {
			"x": position.x,
			"y": position.y
		}
	}
	send(message)

func _on_message_received(message: Variant) -> void:
	var data
	if typeof(message) == TYPE_DICTIONARY:
		data = message
	elif typeof(message) == TYPE_STRING:
		var error = json_parser.parse(message)
		if error == OK:
			data = json_parser.get_data()  # Get the parsed data
			print("Parsed JSON data:", data)
		else:
			print("JSON parse error: ", error)
			return
	else:
		data = null
	
	if data != null and typeof(data) == TYPE_DICTIONARY:
		print("Received message: %s" % var_to_str(data))
		
		# Handle different message types
		match data.get("type"):
			"connection":
				if data.get("status") == "connected":
					print("Successfully connected to server")
			"lobby":
				match data.get("status"):
					"created":
						print("Successfully created lobby: %s" % data.get("lobbyId"))
					"joined":
						print("Successfully joined lobby: %s" % data.get("lobbyId"))
					"player_joined":
						print("Player %s joined the lobby" % data.get("connectionId"))
			"message":
				print("Message from %s: %s" % [data.get("sender"), data.get("content")])
			"position_update":
				var player_id = data.get("playerId")
				var pos = data.get("position")
				if pos != null:
					var position = Vector2(pos.x, pos.y)
					position_update.emit(player_id,position)
			"error":
				print("Error: %s" % data.get("message"))
	else:
		print("Invalid message format: %s" % var_to_str(message))
