extends Control

var server_url = "ws://3.95.7.97:8080"

func _ready() -> void:	
	WebSocketClientHandler.message_received.connect(_on_message_received)
	var error = WebSocketClientHandler.connect_to_url(server_url)
	print("trying to connect to %s" % [server_url])
	if error != OK:
		print("Error connecting to websocket: %s" % [server_url])
	pass # Replace with function body.

func _on_return_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")



func _on_singleplayer_pressed() -> void:
	get_node("SingleplayerOptions").show()
	get_node("MultiplayerOptions").hide()
	pass # Replace with function body.


func _on_multiplayer_pressed() -> void:
	get_node("SingleplayerOptions").hide()
	get_node("MultiplayerOptions").show()
	pass # Replace with function body.

func _on_play_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/game.tscn")
	pass # Replace with function body.


func _on_create_lobby_pressed() -> void:
	WebSocketClientHandler.create_lobby("test")
	pass # Replace with function body.


func _on_join_lobby_pressed() -> void:
	WebSocketClientHandler.join_lobby("test")
	pass # Replace with function body.

func _on_message_received(Variant):
	print(Variant)
