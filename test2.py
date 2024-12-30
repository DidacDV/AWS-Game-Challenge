import socket
import json
import time
import pyxel

from Characters import LocalPlayer, RemotePlayer
from Objects import Bullet, Heal
from Scene import Scene


class App:
    def __init__(self, server_ip, server_port, player_id):
        pyxel.init(160, 120)
        pyxel.load("assets.pyxres")
        self.scene = Scene({"x": 0, "y": 0})
        self.server_address = (server_ip, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setblocking(False)  # Evitar bloqueos al recibir datos
        self.player_id = player_id

        self.last_publish_time = time.time()
        self.publish_interval = 0.05  # Publicar cada 50 ms

        self.projectiles = []

        # Crear jugadores
        local_player = LocalPlayer(80, 60, 8, 8, 2, self)
        remote_player = RemotePlayer(50, 50, 8, 8, 8, self.scene)
        self.players = [local_player, remote_player]

        self.fullscreen = False
        pyxel.fullscreen(self.fullscreen)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def send_position(self):
        """Envia la posición del jugador local al servidor."""
        current_time = time.time()
        if current_time - self.last_publish_time >= self.publish_interval:
            message = {
                "id": self.player_id,
                "position": {"x": self.players[0].x, "y": self.players[0].y}  # Jugador local
            }
            self.client_socket.sendto(json.dumps(message).encode("utf-8"), self.server_address)
            self.last_publish_time = current_time

    def receive_positions(self):
        """Recibe y actualiza las posiciones de los jugadores remotos desde el servidor."""
        try:
            data, _ = self.client_socket.recvfrom(1024)
            positions = json.loads(data.decode("utf-8"))
            for player_id, position in positions.items():
                if player_id != self.player_id:  # Ignorar posición del jugador local
                    self.players[1].x = position["x"]  # Actualizar posición remota
                    self.players[1].y = position["y"]
        except BlockingIOError:
            pass  # No hay datos disponibles, continuar sin bloquear

    def update(self):
        """Actualiza la lógica del juego."""
        self.send_position()  # Enviar posición local al servidor
        self.receive_positions()  # Recibir actualizaciones remotas

        # Actualizar todos los jugadores
        for player in self.players:
            player.update()

        # Actualizar proyectiles
        self.projectiles = [b for b in self.projectiles if b.is_active()]
        for projectile in self.projectiles:
            projectile.update()
            for character in self.players:
                if character != projectile.owner and character.hit(projectile):
                    print("hit")

        # Actualizar escena
        self.scene.update(self.players[0])

        # Actualizaciones de la aplicación
        if pyxel.btnp(pyxel.KEY_F11):
            self.fullscreen = not self.fullscreen
            pyxel.fullscreen(self.fullscreen)
        if pyxel.btnp(pyxel.KEY_Q, 1, 1):
            pyxel.quit()
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.projectiles.append(Bullet(self.players[0].x, self.players[0].y, pyxel.mouse_x, pyxel.mouse_y, 4, self.players[0]))
        if pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):
            self.projectiles.append(Heal(self.players[0].x, self.players[0].y, pyxel.mouse_x, pyxel.mouse_y, 4, self.players[0]))

    def draw(self):
        """Dibuja los elementos del juego."""
        pyxel.cls(0)
        self.scene.draw()
        for character in self.players:
            character.draw()
        for projectile in self.projectiles:
            projectile.draw()


# Configuración del cliente
server_ip = "13.39.48.250"  # IP pública del servidor EC2
server_port = 12345  # Puerto del servidor
player_id = "player2"  # Identificador único del jugador

App(server_ip, server_port, player_id)
