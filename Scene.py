import pyxel


class Scene:
    def __init__(self, camera):
        self.camera = camera
        pyxel.load("assets.pyxres")

    def update(self, player):
        # Update camera position to follow player, keeping it within map boundaries
        self.camera["x"] = max(0, min(player.x - 80, pyxel.tilemaps[0].width * 8 - 160))
        self.camera["y"] = max(0, min(player.y - 60, pyxel.tilemaps[0].height * 8 - 120))

    def draw(self):
        pyxel.bltm(0, 0, 0, self.camera["x"], self.camera["y"], 160, 120)