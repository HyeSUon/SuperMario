from pico2d import *

import game_framework
import game_world
import server
class Grass:
    def __init__(self, center = 2070, y = 40):
        self.left = 0
        self.right = 4140
        self.bottom = 40
        self.top = 80

    def update(self):
        self.cleft = self.left - server.background.window_left
        self.cright = self.right - server.background.window_left
        self.cbottom = self.bottom - server.background.window_bottom
        self.ctop = self.top - server.background.window_bottom

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.cleft,self.cbottom,self.cright,self.ctop