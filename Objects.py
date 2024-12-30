import math

import pyxel
from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y


    @abstractmethod
    def update(self):
        pass

    def draw(self):
        pyxel.pset(self.x, self.y, 2)

    def is_active(self):
        return self.lifetime > 0

class Bullet(Object):
    def __init__(self, x, y, target_x, target_y, speed, Owner):
        super().__init__(x, y, 1, 1, 2)
        dx = target_x - x
        dy = target_y - y
        self.angle = pyxel.atan2(dy, dx)
        self.speed = speed
        self.lifetime = 60
        self.trajectory = [(x,y)]
        self.owner = Owner

    def update(self):
        self.x += self.speed * pyxel.cos(self.angle)
        self.y += self.speed * pyxel.sin(self.angle)
        self.lifetime -= 1
        self.trajectory.append((self.x, self.y))
        if len(self.trajectory) > 10:
            self.trajectory.pop(0)

class Heal(Object):
    def __init__(self, x, y, target_x, target_y, speed, Owner):
        super().__init__(x, y, 1, 1, 2)
        dx = target_x - x
        dy = target_y - y
        self.angle = pyxel.atan2(dy, dx)
        self.speed = speed
        self.lifetime = 60
        self.trajectory = [(x,y)]
        self.owner = Owner

    def update(self):
        self.x += self.speed * pyxel.cos(self.angle)
        self.y += self.speed * pyxel.sin(self.angle)
        self.lifetime -= 1
        self.trajectory.append((self.x, self.y))
        if len(self.trajectory) > 10:
            self.trajectory.pop(0)