class_name Game
extends Node2D

var server_url = "wss://khplzh5o84.execute-api.eu-west-3.amazonaws.com/production/"
var messageToSend = ""
var remote_players = {}
var mode : String

func _ready() -> void:	
	WebSocketClientHandler.connected_to_server.connect(_on_websocket_client_connected_to_server)
	WebSocketClientHandler.connection_closed.connect(_on_websocket_client_connection_close)
	WebSocketClientHandler.message_received.connect(_on_message_received)
	WebSocketClientHandler.position_update.connect(_on_remote_player_position_update)
	WebSocketClientHandler.player_joined.connect(_on_remote_player_lobby_joined)
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
					_on_remote_player_lobby_joined("test")
					pass
				KEY_T:
					var test_post = Vector2(5,6)
					remote_players["test"].update_position(test_post)
	
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
	remote_players[playerId].update_position(newPosition)
	
func _on_remote_player_lobby_joined(player_id: String):
	var new_player = Player.new_player()
	remote_players[player_id] = new_player
	add_child(new_player)
