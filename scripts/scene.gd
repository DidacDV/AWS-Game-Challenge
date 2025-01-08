extends Node2D

var server_url = "ws://44.204.229.199:8080"
var messageToSend = ""
# Called when the node enters the scene tree for the first time.

@onready var _client : WebSocketClient = $WebSocketClient

func _ready() -> void:	
	_connect_to_ws_server()
	print("Tried connection")
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
	
func _connect_to_ws_server():
	var error = _client.connect_to_url(server_url)
	print("trying to connect to %s" % [server_url])
	if error != OK:
		print("Error connecting to websocket: %s" % [server_url])

func _on_websocket_client_connection_close():
	var ws = _client.get_socket()
	print("Client disconnected with code: %s, reason %s" % [ws.get_close_code(), ws.get_close_reason()])

func _on_websocket_client_connected_to_server():
	print("Client connected...")


func _on_web_socket_handler_connection_closed() -> void:
	pass # Replace with function body.
