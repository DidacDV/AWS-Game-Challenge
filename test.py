import pyxel

import Characters
from Objects import Bullet, Heal
from Characters import LocalPlayer, RemotePlayer, Entity
from Scene import Scene


class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("assets.pyxres")
        self.scene = Scene({"x": 0, "y": 0})
        local_player = LocalPlayer(80, 60, 8, 8, 2)
        remote_player = RemotePlayer(50, 50, 8, 8, 8, self.scene)
        self.projectiles = []
        self.players = [local_player, remote_player]
        self.fullscreen = False
        pyxel.fullscreen(self.fullscreen)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

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


App()
