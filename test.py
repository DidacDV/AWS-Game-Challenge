import pyxel

class Login:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.escala = 1
        self.selected = None
        self.write = False
        self.mayus = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
        self.altura = 320 * self.escala
        self.largura = 180 * self.escala
        self.fullscreen = True
        
        pyxel.init(self.altura, self.largura, title="Login")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

        if pyxel.btnp(pyxel.KEY_Q) and not self.write:
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_F11) and not self.write:
            self.fullscreen = not self.fullscreen
            pyxel.fullscreen(self.fullscreen)
        if pyxel.btnp(pyxel.KEY_CAPSLOCK):
            self.mayus = not self.mayus

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.x, self.y = pyxel.mouse_x, pyxel.mouse_y
            if 50 <= self.x <= 250:
                if 50 <= self.y <= 70:
                    self.selected = "username"
                    self.write = True
                elif 100 <= self.y <= 120:
                    self.selected = "password"
                    self.write = True
                else:
                    self.selected = None
                    self.write = False
            else:
                self.selected = None
                self.write = False

        if self.selected:
            if pyxel.btnp(pyxel.KEY_BACKSPACE):
                if self.selected == "username":
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            
            for key in range(ord('0'), ord('9') + 1):
                if pyxel.btnp(key):
                    if self.selected == "username":
                        self.username += chr(key)
                    elif self.selected == "password":
                        self.password += chr(key)
            
            for key in range(ord('a'), ord('z') + 1):
                if pyxel.btnp(key):
                    char = chr(key)
                    if not self.mayus:
                        char = char.lower()
                    else:
                        char = char.upper()
                    if self.selected == "username":
                        self.username += char
                    elif self.selected == "password":
                        self.password += char

    def draw(self):
        pyxel.cls(0)
        pyxel.rectb(50, 50, 200, 20, 7)
        pyxel.rectb(50, 100, 200, 20, 7)
        
        pyxel.text(50, 40, "Username:", 7)
        pyxel.text(50, 90, "Password:", 7)
        pyxel.text(60, 56, self.username, 7)
        pyxel.text(60, 106, "*" * len(self.password), 7)
        
        if self.selected and self.cursor_visible:
            if self.selected == "username":
                cursor_x = 60 + len(self.username) * 4  
                pyxel.rect(cursor_x, 56, 1, 7, 7)
            else:
                cursor_x = 60 + len(self.password) * 4
                pyxel.rect(cursor_x, 106, 1, 7, 7)
        
Login()