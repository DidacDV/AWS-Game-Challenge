import pyxel 

class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class Inventory:
    def __init__(self):
        self.items = {}
        self.max_items = 3
        self.spaces = [None] * self.max_items #intialize empty list with max items size

    def add_item(self, name):
        if (len(self.items) <= self.max_items):
            if name in self.items:
                self.items[name] += 1
            else: 
                self.items[name] = 1
                for i in range(self.max_items):
                    if self.spaces[i] == None:
                        self.spaces[i] = name #put the name to draw it correctly from its name
                        break

        else:
            print("Inventory is full. Cannot add more items.")


    def reduce_quantity_by_one(self, name):
        if name in self.items:
            self.items[name] -= 1
            if self.items[name] == 0:
                self.delete_item(name)
        else:
            print(f"Item '{name}' not found in inventory.")


    def delete_item(self, name): #we dont check errors since they are already checked in reduce_quantity_by_one
        del self.items[name]
        for i in range(self.max_items):
            if self.spaces[i] == name:
                self.spaces[i] = None
                break


    def get_all_items(self):
        result = []
        for name, quantity in self.items.items():
            result.append(name,quantity)
        print(result)

    def get_quantity(self, name):
        if name in self.items:
            return self.items[name]
        else:
            print(f"Item '{name}' not found in inventory.")

    def draw(self):
        pyxel.rectb(4, 8, self.max_items * 16, 16, 7)
        pyxel.text(0, 0, "Inventory", 2)

        self.add_item("item1")
        self.add_item("item2")
        self.add_item("item3")
        for i in range(self.max_items):
            if self.spaces[i] is not None:
                name = self.spaces[i]
                quantity = self.items[name] #to be used !
                sprite_values = self.select_sprite_item(name)
                x = 4 + i * 16 + (16 - sprite_values[2]) / 2  #where rectangle starts + i * width of each item slot + center the sprite horizontally
                y = 8 + (16 - sprite_values[3]) / 2  #height where it starts + center the sprite vertically within a 16px height (height of the item slot)
                pyxel.blt(x, y, 0, sprite_values[0], sprite_values[1], sprite_values[2], sprite_values[3], 0)


        for i in range(1, self.max_items):  
            x = 4 + i * 16 - 1 # 4 -> since inventory starts at 4, 16 -> width of each item slot, -1-> omit last and first borders
            pyxel.line(x, 9, x, 22, 13) 

    def select_sprite_item(self, name):
        values = [0, 0, 0, 0]
        if name == "item1":
            values = [40, 64, 8, 8]
        elif name == "item2":
            values = [48, 64, 8, 8]
        elif name == "item3":
            values = [40, 72, 8, 8]        
        elif name == "item4":
            values = [48, 72, 8, 8]
        else:
            print("Item not found in the sprites !!.")
            values = 0
        return values
        