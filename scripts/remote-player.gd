extends CharacterBody2D

func update_position(new_position: Vector2):
	# Update the player's position based on data from the MQTT server
	global_position = new_position
