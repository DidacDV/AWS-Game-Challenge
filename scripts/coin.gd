extends Area2D

func _on_body_entered(body: Node2D) -> void:
	var mqtt = get_node("/root/Game/MQTTHandler")
	mqtt.on_message_received({"x": 1, "y": 7})
	queue_free()
	pass # Replace with function body.
