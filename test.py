import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.x = 50
        self.y = 50
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_S):
            self.y -= 1
        if pyxel.btnp(pyxel.KEY_W):
            self.y += 1


    def draw(self):
        pyxel.cls(0)
        pyxel.text(self.x,self.y,"Hello World!",5)


App()
