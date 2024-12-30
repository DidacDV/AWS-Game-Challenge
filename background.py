import pyxel
import random

HEIGHT = 120
WIDTH = 160

def getStarValues():
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)
    speed = random.uniform(1, 1.5)
    return {"x": x, "y": y, "speed": speed}

class Background:
    def __init__(self):
        self.snow = [getStarValues() for _ in range(50)]

    def update(self):
        for snow in self.snow:
            snow["y"] += snow["speed"]
            if snow["y"] > HEIGHT - 1:  #if snow goes beyond screen reset to begin
                snow["x"] = random.randint(0, WIDTH - 1)
                snow["y"] = 0
                snow["speed"] = random.uniform(0.5, 1.5)

    def draw(self):
        for snow in self.snow:
            pyxel.pset(snow["x"], snow["y"],  7)
