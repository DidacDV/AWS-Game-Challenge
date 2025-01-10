extends Control


var server_url = "wss://yi4wag7bw5.execute-api.us-east-1.amazonaws.com/production/"

func _ready() -> void:	
	WebSocketClientHandler.message_received.connect(_on_message_received)
	WebSocketClientHandler.connected_to_server.connect(_on_websocket_client_connected_to_server)
	WebSocketClientHandler.connection_closed.connect(_on_websocket_client_connection_close)
	pass # Replace with function body.

func _on_return_pressed() -> void:
	WebSocketClientHandler.close()
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")



func _on_singleplayer_pressed() -> void:
	WebSocketClientHandler.close()
	get_node("SingleplayerOptions").show()
	get_node("MultiplayerOptions").hide()
	pass # Replace with function body.


func _on_multiplayer_pressed() -> void:
	var error = WebSocketClientHandler.connect_to_url(server_url)
	print("trying to connect to %s" % [server_url])
	if error != OK:
		print("Error connecting to websocket: %s" % [server_url])
	get_node("SingleplayerOptions").hide()
	get_node("MultiplayerOptions").show()
	pass # Replace with function body.

func _on_play_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/game.tscn")
	pass # Replace with function body.


func _on_create_lobby_pressed() -> void:
	print("Creating lobby")
	WebSocketClientHandler.create_lobby("test")
	pass # Replace with function body.


func _on_join_lobby_pressed() -> void:
	WebSocketClientHandler.join_lobby("test")
	WebSocketClientHandler.setLobbyId("test") 
	get_tree().change_scene_to_file("res://scenes/game.tscn")
	pass # Replace with function body.

func _on_message_received(message):
	print(message)
	
func _on_websocket_client_connection_close():
	var ws = WebSocketClientHandler.get_socket()
	print("Client disconnected with code: %s, reason %s" % [ws.get_close_code(), ws.get_close_reason()])
	var error = WebSocketClientHandler.connect_to_url(server_url)
	print("trying to connect to %s" % [server_url])
	if error != OK:
		print("Error connecting to websocket: %s" % [server_url])
		
func _on_websocket_client_connected_to_server():
	print("Client connected...")
