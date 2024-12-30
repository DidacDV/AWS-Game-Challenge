import socket
import json
import time
import pyxel

from Characters import LocalPlayer, RemotePlayer
from Objects import Bullet, Heal
from Scene import Scene


class App:
    def __init__(self, server_ip, server_port, shoot_server_ip, shoot_server_port, player_id):
        pyxel.init(160, 120)
        pyxel.load("assets.pyxres")
        self.scene = Scene({"x": 0, "y": 0})
        self.server_address = (server_ip, server_port)
        self.shoot_server_address = (shoot_server_ip, shoot_server_port)

        # Sockets para posición y disparos
        self.position_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.position_socket.setblocking(False)  # Evitar bloqueos al recibir datos
        self.shoot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.shoot_socket.setblocking(False)

        self.player_id = player_id
        self.is_shooting = False  # Estado actual de disparo

        self.last_publish_time = time.time()
        self.publish_interval = 0.05  # Publicar cada 50 ms

        self.projectiles = []

        # Crear jugadores
        local_player = LocalPlayer(80, 60, 8, 8, 2, self)
        remote_player = RemotePlayer(80, 60, 8, 8, 8, self.scene)
        self.players = [local_player, remote_player]

        self.fullscreen = False
        pyxel.fullscreen(self.fullscreen)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def send_position(self):
        """Envía la posición del jugador local al servidor de posiciones."""
        current_time = time.time()
        if current_time - self.last_publish_time >= self.publish_interval:
            message = {
                "id": self.player_id,
                "position": {"x": self.players[0].x, "y": self.players[0].y}  # Jugador local
            }
            self.position_socket.sendto(json.dumps(message).encode("utf-8"), self.server_address)
            self.last_publish_time = current_time

    def send_shooting_event(self, is_shooting, target_x=None, target_y=None):
        """Envía un evento de disparo al servidor de disparos con dirección opcional."""
        if self.is_shooting != is_shooting:
            shooting_data = {
                "id": self.player_id,
                "shooting": is_shooting,
                "target": {"x": target_x, "y": target_y} if target_x and target_y else None
            }
            self.shoot_socket.sendto(json.dumps(shooting_data).encode("utf-8"), self.shoot_server_address)
            self.is_shooting = is_shooting

    def receive_positions(self):
        """Recibe y actualiza las posiciones de los jugadores remotos desde el servidor."""
        try:
            data, _ = self.position_socket.recvfrom(1024)
            positions = json.loads(data.decode("utf-8"))
            for player_id, position in positions.items():
                if player_id != self.player_id:  # Ignorar posición del jugador local
                    self.players[1].x = position["x"]  # Actualizar posición remota
                    self.players[1].y = position["y"]
        except BlockingIOError:
            pass  # No hay datos disponibles, continuar sin bloquear

    def receive_shooting_states(self):
        """Recibe los estados de disparo y las direcciones de otros jugadores."""
        try:
            data, _ = self.shoot_socket.recvfrom(1024)
            shooting_states = json.loads(data.decode("utf-8"))["shooting_states"]

            # Verificar si el jugador remoto está disparando
            for player_id, shooting_data in shooting_states.items():
                if player_id != self.player_id and shooting_data["shooting"]:
                    target = shooting_data.get("target", {})
                    self.projectiles.append(Bullet(
                        self.players[1].x,
                        self.players[1].y,
                        target.get("x", self.players[1].x + 10),
                        target.get("y", self.players[1].y),
                        4,
                        self.players[1]
                    ))
        except BlockingIOError:
            pass  # No hay datos disponibles, continuar sin bloquear

    def update(self):
        """Actualiza la lógica del juego."""
        self.send_position()  # Enviar posición local al servidor
        self.receive_positions()  # Recibir actualizaciones remotas
        self.receive_shooting_states()  # Recibir eventos de disparo

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
            self.projectiles.append(
                Bullet(self.players[0].x, self.players[0].y, pyxel.mouse_x, pyxel.mouse_y, 4, self.players[0]))
            self.send_shooting_event(True, pyxel.mouse_x, pyxel.mouse_y)  # Enviar evento de disparo con dirección
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.send_shooting_event(False)  # Detener el evento de disparo

    def draw(self):
        """Dibuja los elementos del juego."""
        pyxel.cls(0)

        # Dibuja el mapa según la cámara
        self.scene.draw()

        # Dibuja jugadores ajustados a la cámara
        for character in self.players:
            adjusted_x = character.x - self.scene.camera["x"]
            adjusted_y = character.y - self.scene.camera["y"]
            pyxel.blt(adjusted_x, adjusted_y, 0, 56, 56, 8, 8)  # Cambiar las coordenadas del sprite según corresponda
            # Dibujar barra de vida
            pyxel.rect(adjusted_x, adjusted_y - 3, 8, 2, 8)  # Fondo gris
            pyxel.rect(adjusted_x, adjusted_y - 3, int(8 * (character.health / character.max_health)), 2, 11)  # Verde

        # Dibuja proyectiles ajustados a la cámara
        for projectile in self.projectiles:
            adjusted_x = projectile.x - self.scene.camera["x"]
            adjusted_y = projectile.y - self.scene.camera["y"]
            if 0 <= adjusted_x <= 160 and 0 <= adjusted_y <= 120:  # Dibuja solo si está visible
                pyxel.blt(adjusted_x, adjusted_y, 0, 40, 64, 8, 8, 0)  # Cambiar por las coordenadas reales


# Configuración del cliente
server_ip = "13.39.48.250"  # IP pública del servidor de posiciones
server_port = 12345  # Puerto del servidor de posiciones
shoot_server_ip = "35.180.116.17"  # IP pública del servidor de disparos
shoot_server_port = 12346  # Puerto del servidor de disparos
player_id = "player2"  # Identificador único del jugador

App(server_ip, server_port, shoot_server_ip, shoot_server_port, player_id)
