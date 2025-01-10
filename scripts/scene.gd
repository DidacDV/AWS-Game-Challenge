extends Node2D

var server_url = "wss://yi4wag7bw5.execute-api.us-east-1.amazonaws.com/production/"
var messageToSend = ""
@export var Player: PackedScene
var remote_players = {}
# Called when the node enters the scene tree for the first time.

func _ready() -> void:	
	WebSocketClientHandler.connected_to_server.connect(_on_websocket_client_connected_to_server)
	WebSocketClientHandler.connection_closed.connect(_on_websocket_client_connection_close)
	WebSocketClientHandler.message_received.connect(_on_message_received)
	WebSocketClientHandler.position_update.connect(_on_remote_player_position_update)
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
	
func _input(event):
	# Detect key press
	if event is InputEventKey:
		if event.pressed:  # Check if the key is being pressed
			match event.keycode:
				KEY_Q:
					print("Sending position")
					var position = $Player.position
					WebSocketClientHandler.send_position("test", position)

	
func _connect_to_ws_server():
	var error = WebSocketClientHandler.connect_to_url(server_url)
	print("trying to connect to %s" % [server_url])
	if error != OK:
		print("Error connecting to websocket: %s" % [server_url])

func _on_websocket_client_connection_close():
	var ws = WebSocketClientHandler.get_socket()
	print("Client disconnected with code: %s, reason %s" % [ws.get_close_code(), ws.get_close_reason()])

func _on_websocket_client_connected_to_server():
	print("Client connected...")


func _on_web_socket_handler_connection_closed() -> void:
	pass # Replace with function body.
	
func _on_message_received(Variant):
	print(Variant)
	
func _on_remote_player_position_update(playerId: String, newPosition: Vector2):
	print("Updating position")
	$RemotePlayer.position = newPosition
