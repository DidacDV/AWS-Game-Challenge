extends Node
class_name WebSocketClient 

var socket = WebSocketPeer.new()
var last_state = WebSocketPeer.STATE_CLOSED
var json_parser = JSON.new()

signal connected_to_server()
signal connection_closed()
signal message_received(message: Variant)


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
		message_received.emit(get_message())
	
func send(message) -> int:
	if typeof(message) == TYPE_STRING:
		return socket.send_text(message)
	return socket.send(var_to_bytes(message))

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
	socket.close(code, reason)
	last_state = socket.get_ready_state()

func get_socket() -> WebSocketPeer:
	return socket
	
func _process(delta):
	poll()

func create_lobby(lobby_id: String) -> void:
	var message = {
		"action": "create_lobby",
		"lobbyId": lobby_id
		}
	send(message)

func join_lobby(lobby_id: String) -> void:
	var message = {
		"action": "join_lobby",
		"lobbyId": lobby_id
		}
	send(message)

func send_lobby_message(lobby_id: String, message_payload: String) -> void:
	var message = {
		"action": "send_message",
		"lobbyId": lobby_id,
		"payload": message_payload 
		}
	send(message)

func _on_message_received(message: Variant) -> void:
	var data
	if typeof(message) == TYPE_DICTIONARY:
		data = message
	elif typeof(message) == TYPE_STRING:
		var result = json_parser.parse(message)
		if result.error == OK:
			data = result.result
	else:
		data = null
	
	if data != null and typeof(data) == TYPE_DICTIONARY:
		print("Received valid message: %s" % var_to_str(data))
	else:
		print("Invalid message format: %s" % var_to_str(message))
