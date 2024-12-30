import pyxel
import math
from background import Background
from classMenu import ClassMenu

GUN_LENGTH = 10
GUN_ADDED_X = 8
GUN_ADDED_Y = 22
BODY_WIDTH = 2  # Width of the character body
PINK = 8




class App:
    def __init__(self):
        self.started = False
        self.class_menu = ClassMenu()
        pyxel.init(160, 120)
        pyxel.load("player.pyxres")
        self.x = 50
        self.y = 50
        self.bg = Background()
        self.class_selected = -1
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if not self.started:
            if self.class_menu.update_menu():
                self.started = True
                self.class_selected = self.class_menu.get_selected_class()
        else:
            print(self.class_selected)
            self.update_game()
        self.bg.update()

    def update_game(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 2
        self.bg.update()
    
    def draw(self):
        pyxel.cls(0)
        self.bg.draw()

        if not self.started:
            self.class_menu.draw_menu()
        else: 
            self.draw_game()

    def draw_game(self):
        #calculate for right and left
        values_right = calculateGunPosition(self.x + BODY_WIDTH, self.y, pyxel.mouse_x, pyxel.mouse_y)
        values_left = calculateGunPosition(self.x - BODY_WIDTH, self.y, pyxel.mouse_x, pyxel.mouse_y)
            
        gun_x_right = values_right[0]
        gun_y_right = values_right[1]
        gun_x_left = values_left[0]
        gun_y_left = values_left[1]
            
        #draw right
        pyxel.line(self.x + BODY_WIDTH - 1 + GUN_ADDED_X, self.y + GUN_ADDED_Y, gun_x_right, gun_y_right, PINK)
        pyxel.line(self.x + BODY_WIDTH + GUN_ADDED_X, self.y + 5 + GUN_ADDED_Y, gun_x_right, gun_y_right, PINK)
            
        #draw left
        pyxel.line(self.x - BODY_WIDTH + GUN_ADDED_X, self.y + GUN_ADDED_Y, gun_x_left, gun_y_left, PINK)
        pyxel.line(self.x - BODY_WIDTH + GUN_ADDED_X, self.y + 5 + GUN_ADDED_Y, gun_x_left, gun_y_left, PINK)
            
        pyxel.blt(self.x, self.y, 0, 0, 0, 32, 40, 0)


def calculateGunPosition(x1, y1, mouse_x, mouse_y):
    angle = math.atan2(mouse_y - y1, mouse_x - x1)
    gun_x = x1 + GUN_ADDED_X + GUN_LENGTH * math.cos(angle)
    gun_y = y1 + GUN_ADDED_Y + GUN_LENGTH * math.sin(angle)
    return [gun_x, gun_y]

App()