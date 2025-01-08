extends Node
class_name WebSocketClient 

var socket = WebSocketPeer.new()
var last_state = WebSocketPeer.STATE_CLOSED

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
			print("it connected")
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
