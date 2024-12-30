import math
from typing import override

import pyxel
from abc import ABC, abstractmethod

HEIGHT = 8
WIDTH = 8

class Object(ABC):
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    def is_active(self):
        return self.lifetime > 0


class Projectile(Object):
    def __init__(self, x, y, target_x, target_y, speed, Owner):
        super().__init__(x, y, 2)
        dx = target_x - x
        dy = target_y - y
        self.angle = pyxel.atan2(dy, dx)
        self.speed = speed
        self.lifetime = 60
        self.trajectory = [(x,y)]
        self.owner = Owner

    @abstractmethod
    def draw(self):
        pass

    def update(self):
        self.x += self.speed * pyxel.cos(self.angle)
        self.y += self.speed * pyxel.sin(self.angle)
        self.lifetime -= 1
        self.trajectory.append((self.x, self.y))
        if len(self.trajectory) > 10:
            self.trajectory.pop(0)

class Bullet(Projectile):
    def __init__(self, x, y, target_x, target_y, speed, Owner):
        super().__init__(x, y, target_x, target_y, speed, Owner)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 40, 64, HEIGHT, WIDTH, rotate=math.degrees(self.angle))

class Heal(Projectile):
    def __init__(self, x, y, target_x, target_y, speed, Owner):
        super().__init__(x, y, target_x, target_y, speed, Owner)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 7, 7, HEIGHT, WIDTH)
