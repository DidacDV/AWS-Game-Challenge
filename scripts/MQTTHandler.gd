extends Node

var remote_player
var broker_url = "tcp://52.47.154.254:1883/"  # Replace with your broker's URL

func _ready():
	# Set Last Will message before connecting
	$MQTT.set_last_will("game/player1", "Player disconnected", false, 0)

	# Connect to the MQTT broker
	$MQTT.connect_to_broker(broker_url)

	# Subscribe to the topic for remote player updates
	$MQTT.subscribe("game/player2", 0)

	# Connect signal to handle received messages
	$MQTT.connect("received_message", self, "_on_message_received")

	# Reference the RemotePlayer node
	remote_player = get_node("/root/Game/RemotePlayer")

func _on_message_received(topic, message):
	var data = JSON.parse(message).result
	if data.has("x") and data.has("y"):
		if remote_player:
			remote_player.update_position(Vector2(data["x"], data["y"]))
		else:
			print("RemotePlayer node is missing!")

func _process(delta):
	# Publish position of the local player to the broker periodically
	publish_position(local_player.x, local_player.y)

# Publish player position to the broker
func publish_position(x, y):
	var data = {"x": x, "y": y}
	var message = JSON.print(data)
	$MQTT.publish("game/player1", message, false, 0)
