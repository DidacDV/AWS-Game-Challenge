import pyxel as px


class App:
    def __init__(self):
        self.height = 160
        self.width = 90

        self.fullscreen = False

        self.x = 50
        self.y = 50

        px.init(self.width, self.height, title="Login") 
        px.run(self.update, self.draw)
        

    def update(self):
        if px.btnp(px.KEY_Q):
            px.quit()
        if px.btnp(px.KEY_S):
            self.y -= 1
        if px.btnp(px.KEY_W):
            self.y += 1
        if px.btnp(px.KEY_F11):
            self.fullscreen = not self.fullscreen
            px.fullscreen(self.fullscreen)
        
        

    def draw(self):
        px.cls(0)
        px.text(self.x, self.y, "Hello World!", 5)

App()