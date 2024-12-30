import pyxel
import paho.mqtt.client as mqtt
import json
import time

class MultiplayerGame:
    def __init__(self, broker, port, topic_publish, topic_subscribe):
        pyxel.init(160, 120, title="Multiplayer Game")
        self.local_player = {"x": 80, "y": 60}  # Posición inicial local
        self.remote_player = {"x": 0, "y": 0}  # Posición inicial remota
        self.remote_target = {"x": 0, "y": 0}  # Posición objetivo para interpolación
        self.last_publish_time = time.time()
        self.publish_interval = 0.05  # 50 ms (ajustable según necesidad)

        # Configuración MQTT
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(broker, port, 60)
        self.client.subscribe(topic_subscribe, qos=0)  # Reducir QoS a 0 para minimizar latencia
        self.topic_publish = topic_publish

        # Iniciar cliente MQTT
        self.client.loop_start()

        pyxel.run(self.update, self.draw)

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload)
            # Actualizar la posición objetivo del jugador remoto
            if "x" in data and "y" in data:
                self.remote_target["x"] = data["x"]
                self.remote_target["y"] = data["y"]
                print(f"Jugador remoto actualizado: {self.remote_target}")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar el mensaje: {e}")

    def interpolate(self, target, current, alpha=0.1):
        """Interpolar suavemente entre la posición actual y la posición objetivo."""
        return current + alpha * (target - current)

    def update(self):
        # Actualizar posición del jugador remoto con interpolación
        self.remote_player["x"] = self.interpolate(self.remote_target["x"], self.remote_player["x"])
        self.remote_player["y"] = self.interpolate(self.remote_target["y"], self.remote_player["y"])

        dx = dy = 0
        if pyxel.btn(pyxel.KEY_W): dy -= 1
        if pyxel.btn(pyxel.KEY_S): dy += 1
        if pyxel.btn(pyxel.KEY_A): dx -= 1
        if pyxel.btn(pyxel.KEY_D): dx += 1

        if dx != 0 or dy != 0:
            # Actualizar posición local
            self.local_player["x"] += dx
            self.local_player["y"] += dy

            # Publicar posición local al broker a intervalos
            current_time = time.time()
            if current_time - self.last_publish_time >= self.publish_interval:
                self.client.publish(self.topic_publish, json.dumps(self.local_player), qos=0)
                self.last_publish_time = current_time

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
# Jugador 1:
# topic_publish = "game/player1"
# topic_subscribe = "game/player2"

# Jugador 2:
# topic_publish = "game/player2"
# topic_subscribe = "game/player1"

# Cambiar según el jugador
topic_publish = "game/player1"
topic_subscribe = "game/player2"

MultiplayerGame(broker, port, topic_publish, topic_subscribe)
