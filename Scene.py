import pyxel


class Scene:
    def __init__(self, camera):
        self.camera = camera
        pyxel.load("assets.pyxres")

    def update(self, player, smooth_camera=False):
        """
        Actualiza la posición de la cámara para seguir al jugador.
        Si `smooth_camera` es True, la cámara se mueve suavemente.
        """
        target_x = max(0, min(player.x - 80, pyxel.tilemaps[0].width * 8 - 160))
        target_y = max(0, min(player.y - 60, pyxel.tilemaps[0].height * 8 - 120))

        if smooth_camera:
            # Movimiento suave de la cámara
            speed = 0.1  # Ajusta este valor para más o menos suavidad
            self.camera["x"] += (target_x - self.camera["x"]) * speed
            self.camera["y"] += (target_y - self.camera["y"]) * speed
        else:
            # Movimiento brusco de la cámara
            self.camera["x"] = target_x
            self.camera["y"] = target_y

    def draw(self):
        """
        Dibuja el mapa en función de la posición de la cámara.
        """
        pyxel.bltm(0, 0, 0, self.camera["x"], self.camera["y"], 160, 120)

    def debug_draw(self):
        """
        Opcional: Dibuja coordenadas para depuración.
        """
        pyxel.text(5, 5, f"Camera: ({int(self.camera['x'])}, {int(self.camera['y'])})", 7)
