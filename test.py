import pyxel

class Login:
    def __init__(self):
        self.escala = 1

        self.altura = 320 * self.escala
        self.largura = 180 * self.escala

        self.x = 50 * self.escala
        self.y = 50 * self.escala

        self.fullscreen = True

        pyxel.init(self.altura, self.largura, title="Login")
        pyxel.run(self.update, self.draw)        

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_S):
            self.y -= 1
        if pyxel.btnp(pyxel.KEY_W):
            self.y += 1
        if pyxel.btnp(pyxel.KEY_F11):
            self.fullscreen = not self.fullscreen
            pyxel.fullscreen(self.fullscreen)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(self.x,self.y,"Hello World!",5)


Login()
