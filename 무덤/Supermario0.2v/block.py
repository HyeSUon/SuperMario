import random
from pico2d import *
import game_world
import game_framework





import random
from pico2d import *
import game_world
import game_framework

class Floor:
    image = None

    def __init__(self, x = 0, y = 0):
        if Floor.image == None:
            Floor.image = load_image('images\item.png')
        self.x, self.y= x, y

    def get_bb(self):
        return self.x - 30, self.y - 20, self.x + 30, self.y + 20

    def draw(self):
        self.image.clip_draw(0, 0, 60, 40, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

