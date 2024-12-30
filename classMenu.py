import pyxel

class ClassMenu:
    def __init__(self):
        self.selected_class = 0

    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_class = (self.selected_class + 1) % 3
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_class = (self.selected_class - 1) % 3
        if pyxel.btnp(pyxel.KEY_RETURN):
            return True
        return False

    def select_sprite_class(self):
        if self.selected_class == 0:
            return [14, 45, 18, 23] #start point in x, start point in y, width and height
        elif self.selected_class == 1:
            return [17, 100, 19, 11]
        elif self.selected_class == 2:
            return [19, 74, 20, 20]
        else:
            return [0, 0, 0, 0]

    def draw_menu(self):
        menu_text = "Choose your class and press Enter"
        class_options = ["1. SwordHandler", "2. GunMaster", "3. Mage"]
        menu_x = (pyxel.width - len(menu_text) * 4) // 2  #center the text since each char is 4 px wide
        pyxel.text(menu_x, 10, menu_text, 7)
        for i, option in enumerate(class_options):
            option_x = (pyxel.width - len(option) * 4) // 2  #center each option
            if self.selected_class == i:
                values = self.select_sprite_class()
                sprite_x = (pyxel.width - values[2]) // 2  #center the sprite horizontally
                sprite_y = 30 + (20 - values[3]) // 2  #center the sprite vertically within a 20px height
                
                #background of the sprite
                pyxel.rect(sprite_x - 2, sprite_y - 2, values[2] + 4, values[3] + 4, 3)
                #actual sprite
                pyxel.blt(sprite_x, sprite_y, 0, values[0], values[1], values[2], values[3], 0)  #draw the symbol of the class
                #border around sprite
                pyxel.rectb(sprite_x - 2, sprite_y - 2, values[2] + 4, values[3] + 4, 7)
                color = 7
            else:
                color = 3
            pyxel.text(option_x, 60 + i * 10, option, color)  #text of the classes goes lower

    def get_selected_class(self):
        return self.selected_class