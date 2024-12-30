import pyxel
import glfw


class App:
    def __init__(self):
        self.escala = 12

        self.altura = 160 * self.escala
        self.largura = 90 * self.escala

        self.x = 50 * self.escala
        self.y = 50 * self.escala

        self.fullscreen = True

        pyxel.init(self.altura, self.largura, title="Login")
        pyxel.run(self.update, self.draw)        

    def updatePantalla(self, escala) :
        self.scale = escala
        self.altura = 160 * self.scale
        self.largura = 90 * self.scale

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            self.updatePantalla(12)
            pyxel.quit()
            pyxel.init(self.altura, self.largura, title="Login")
            pyxel.run(self.update, self.draw)        

        else:
            self.updatePantalla(1)
            pyxel.quit()
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
            self.toggle_fullscreen()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(self.x,self.y,"Hello World!",5)


App()
