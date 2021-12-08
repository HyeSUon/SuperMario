from pico2d import *

import server
import json


class Score:

    def __init__(self):
        self.image = load_image('images\char.png')
        with open('json//number.json', 'r') as f:
            self.number = json.load(f)


    def point_draw(self, name):
        n = 0
        for i in range (0,6):
            s = n%10
            n %= 10
            self.image.clip_draw(self.number[s]['x'], self.number[s]['y'],
                        self.number[s]['w'], self.number[s]['h'], 205+self.number[s]['w']/2-26*i, 559-self.number[s]['h']/2, 26, 22)
    def coin_draw(self):
        pass
    def time_draw(self):
        pass
    def top_score_draw(self):
        pass
    def life_draw(self):
        pass