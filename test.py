import pyxel

from Objects import Bullet, Heal
from Characters import LocalPlayer, RemotePlayer



class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.camera = {"x": 0, "y": 0}
        local_player = LocalPlayer(0, 0, 8 ,8, 2,self.camera)
        remote_player = RemotePlayer(50, 50, 8, 8, 8,self.camera)

        self.projectiles = []
        self.players = [local_player, remote_player]
        self.fullscreen = False
        pyxel.fullscreen(self.fullscreen)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        #Update all characters
        for character in self.players:
            character.update()

        #Update bullets
        self.projectiles = [b for b in self.projectiles if b.is_active()]
        for projectile in self.projectiles:
            projectile.update()
            for character in self.players:
                if character != projectile.owner:
                    if character.hit(projectile):
                        print("hit")
        #Camera update
        self.camera["x"] = max(0, min(self.players[0].x, pyxel.tilemaps[0].width - 160))
        self.camera["y"] = max(0, min(self.players[0].y, pyxel.tilemaps[0].height - 120))


        #App updates
        if pyxel.btnp(pyxel.KEY_F11):
            self.fullscreen = not self.fullscreen
            pyxel.fullscreen(self.fullscreen)
        if pyxel.btnp(pyxel.KEY_Q, 1, 1):
            pyxel.quit()
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.projectiles.append(Bullet(self.players[0].x, self.players[0].y, pyxel.mouse_x, pyxel.mouse_y, 10,
                                           self.players[0]))
        if pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):
            self.projectiles.append(Heal(self.players[0].x, self.players[0].y, pyxel.mouse_x, pyxel.mouse_y, 10,
                                         self.players[0]))


    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, self.camera["x"], self.camera["y"], 160, 120)
        for character in self.players:
            character.draw()
        for projectile in self.projectiles:
            projectile.draw()


App()
