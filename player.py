from pico2d import *

class Mario:
    def __init__(self):
        self.image = load_image('images/mario_temp.png')
        self.x = 100; self.y = 100;
        self.left = 0; self.bottom = 0; self.right = 0; self.top = 0
        self.frame = 0
        self.dir = 0
    def update(self):
        self.frame = (self.frame+1) % 3
        self.x += self.dir
    def draw(self):
        self.image.draw(self.x, self.y)