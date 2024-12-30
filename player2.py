import pyxel
import paho.mqtt.client as mqtt
import json

class MultiplayerGame:
    def __init__(self, broker, port, topic_publish, topic_subscribe):
        pyxel.init(160, 120, title="Multiplayer Game")
        self.local_player = {"x": 80, "y": 60}  # Posición inicial local
        self.remote_player = {"x": 0, "y": 0}  # Posición inicial remota

        # Configuración MQTT
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(broker, port, 60)
        self.client.subscribe(topic_subscribe)
        self.topic_publish = topic_publish

        # Iniciar cliente MQTT
        self.client.loop_start()

        pyxel.run(self.update, self.draw)

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload)
            # Actualizar la posición del jugador remoto
            if "x" in data and "y" in data:
                self.remote_player["x"] = data["x"]
                self.remote_player["y"] = data["y"]
                print(f"Jugador remoto actualizado: {self.remote_player}")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar el mensaje: {e}")

    def update(self):
        dx = dy = 0
        if pyxel.btn(pyxel.KEY_W): dy -= 1
        if pyxel.btn(pyxel.KEY_S): dy += 1
        if pyxel.btn(pyxel.KEY_A): dx -= 1
        if pyxel.btn(pyxel.KEY_D): dx += 1

        if dx != 0 or dy != 0:
            # Actualizar posición local
            self.local_player["x"] += dx
            self.local_player["y"] += dy

            # Publicar posición local al broker
            self.client.publish(self.topic_publish, json.dumps(self.local_player))

    def draw(self):
        pyxel.cls(0)
        # Dibujar jugador local
        pyxel.rect(self.local_player["x"], self.local_player["y"], 8, 8, 11)
        # Dibujar jugador remoto
        pyxel.rect(self.remote_player["x"], self.remote_player["y"], 8, 8, 9)

# Configuración del cliente
broker = "35.180.116.17"  # Cambiar por la IP del broker Mosquitto
port = 1883

# Configuración para cada jugador

# Jugador 2:
topic_publish = "game/player2"
topic_subscribe = "game/player1"


MultiplayerGame(broker, port, topic_publish, topic_subscribe)