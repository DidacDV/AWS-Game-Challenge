from typing import override

import pyxel
import math
from abc import ABC, abstractmethod

import Objects


class Character(ABC):

    def __init__(self, posX, posY, width, height, colour, health=80):
        self.x = posX
        self.y = posY
        self.width = width
        self.height = height
        self.colour = colour
        self.health = health


    @abstractmethod
    def update(self):
        pass

    #For any character, defines the draw method.
    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.colour)


    def hit(self, object):
        return (
                self.x < object.x < self.x + self.width
                and self.y < object.y < self.y + self.height
        )


class Player(Character):
    def __init__(self, posX, posY, width, height, colour, max_health, camera):
        super().__init__(posX,posY, width, height, colour)
        self.max_health = max_health
        self.angle = 0
        self.camera = camera

    @abstractmethod
    def update(self):
        pass

    def draw(self):
        super().draw()
        self.draw_health_bar()

    def draw_health_bar(self):
        bar_width = self.width
        bar_height = 3
        health_ratio = self.health / self.max_health

        # Background of the health bar (empty bar)
        pyxel.rect(self.x, self.y - 5, bar_width, bar_height, 8)  # Gray background

        # Foreground of the health bar (filled portion)
        filled_width = int(bar_width * health_ratio)
        pyxel.rect(self.x, self.y - 5, filled_width, bar_height, 11)  # Green foreground

class LocalPlayer(Player):
    def __init__(self, posX, posY, width, height, colour, camera):
        super().__init__(posX,posY, width, height, colour, 80, camera)


    def update(self):
        dx = pyxel.mouse_x - self.x
        dy = pyxel.mouse_y - self.y
        self.angle = math.atan2(dy, dx)

        if pyxel.btnp(pyxel.KEY_W, 1, 1):
            self.y -= 1
        if pyxel.btnp(pyxel.KEY_A, 1, 1):
            self.x -= 1
        if pyxel.btnp(pyxel.KEY_S, 1, 1):
            self.y += 1
        if pyxel.btnp(pyxel.KEY_D, 1, 1):
            self.x += 1


class RemotePlayer(Player):
    def __init__(self, posX, posY, width, height, colour, camera):
        super().__init__(posX, posY, width, height, colour, 80, camera)
        self.angle = 0

    def update(self):
        return

    @override
    def hit(self, object):
        if self.x < object.x < self.x + self.width and self.y < object.y < self.y + self.height:
            if isinstance(object, Objects.Bullet): self.health -= 1
            elif isinstance(object, Objects.Heal): self.health += 1
