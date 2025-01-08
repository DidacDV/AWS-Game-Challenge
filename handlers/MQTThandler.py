import paho.mqtt.client as mqtt
import json


class MQTTHandler:
    def __init__(self):
        self.broker = "your-ec2-instance-ip"
        self.port = 1883
        self.topic_publish = "game/player1"  # Adjust for your setup
        self.topic_subscribe = "game/player2"

        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, 60)
        self.client.subscribe(self.topic_subscribe, qos=0)
        self.client.loop_start()

    def publish_position(self, x, y):
        payload = json.dumps({"x": x, "y": y})
        self.client.publish(self.topic_publish, payload, qos=0)

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload)
            # You can add inter-process communication or file writes here if needed
        except json.JSONDecodeError as e:
            print(f"Error decoding MQTT message: {e}")


handler = MQTTHandler()
