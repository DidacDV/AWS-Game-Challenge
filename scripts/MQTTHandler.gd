extends Node

# Path to the Python MQTT script
const PYTHON_SCRIPT = "res://handlers/MQTThandler.py"

var python_instance

func _ready():
	# Initialize the Python MQTT handler
	python_instance = load(PYTHON_SCRIPT).new()

func publish_position(position: Vector2):
	# Call the Python function to publish data
	python_instance.publish_position(position.x, position.y)

func on_message_received(data: Dictionary):
	# Parse the received data and update the remote player
	if data.has("x") and data.has("y"):
		var remote_player = get_node("/root/RemotePlayer")
		remote_player.update_position(Vector2(data["x"], data["y"]))
