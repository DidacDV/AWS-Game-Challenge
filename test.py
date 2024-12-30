import json
import time

import pyxel
import paho.mqtt.client as mqtt

import Characters
from Objects import Bullet, Heal
from Characters import LocalPlayer, RemotePlayer, Entity
from Scene import Scene


class App:
    def __init__(self, broker, port, topic_publish, topic_subscribe):
        pyxel.init(160, 120)
        pyxel.load("assets.pyxres")
        self.scene = Scene({"x": 0, "y": 0})
        self.last_publish_time = time.time()
        self.publish_interval = 0.05

        # Configuración MQTT
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(broker, port, 60)
        self.client.subscribe(topic_subscribe, qos=0)  # Reducir QoS a 0 para minimizar latencia
        self.topic_publish = topic_publish
        # Iniciar cliente MQTT
        self.client.loop_start()
        self.projectiles = []



        local_player = LocalPlayer(80, 60, 8, 8, 2, self)
        remote_player = RemotePlayer(50, 50, 8, 8, 8, self.scene)
        self.players = [local_player, remote_player]

        self.fullscreen = False
        pyxel.fullscreen(self.fullscreen)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)



    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload)
            # Actualizar la posición objetivo del jugador remoto
            if "x" in data and "y" in data:
                self.players[1].x = data["x"]
                self.players[1].y = data["y"]
                print(f"Jugador remoto actualizado: {self.players[1].x,self.players[1].y}")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar el mensaje: {e}")

    def publish_position(self,x,y):
        # Publicar posición local al broker a intervalos
        current_time = time.time()
        if current_time - self.last_publish_time >= self.publish_interval:
            self.client.publish(self.topic_publish, json.dumps({"x": x, "y": y}), qos=0)
            self.last_publish_time = current_time

    def update(self):
        #Update all characters
        for player in self.players:
            player.update()

        #Update bullets
        self.projectiles = [b for b in self.projectiles if b.is_active()]
        for projectile in self.projectiles:
            projectile.update()
            for character in self.players:
                if character != projectile.owner:
                    if character.hit(projectile):
                        print("hit")
        #Scene update
        self.scene.update(self.players[0])


        #App updates
        if pyxel.btnp(pyxel.KEY_F11):
            self.fullscreen = not self.fullscreen
            pyxel.fullscreen(self.fullscreen)
        if pyxel.btnp(pyxel.KEY_Q, 1, 1):
            pyxel.quit()
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.projectiles.append(Bullet(self.players[0].x, self.players[0].y, pyxel.mouse_x, pyxel.mouse_y, 4,
                                           self.players[0]))
        if pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):
            self.projectiles.append(Heal(self.players[0].x, self.players[0].y, pyxel.mouse_x, pyxel.mouse_y, 4,
                                         self.players[0]))


    def draw(self):
        pyxel.cls(0)
        self.scene.draw()
        for character in self.players:
            character.draw()

        for projectile in self.projectiles:
            projectile.draw()

broker = "35.180.116.17"  # Cambiar por la IP del broker Mosquitto
port = 1883

# Configuración para cada jugador
# Jugador 1:
# topic_publish = "game/player1"
# topic_subscribe = "game/player2"

# Jugador 2:


# Cambiar según el jugador
topic_publish = "game/player2"
topic_subscribe = "game/player1"


App(broker, port, topic_publish, topic_subscribe)
