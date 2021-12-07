from pico2d import *
import server
import json

with open('json//number.json', 'r') as f:
    number = json.load(f)


class Score:
    def __init__(self):
        self.state = server.name


    def qwer(self):
        print(self.state)







    def point(image):
        for i in range (0,6):
            image.clip_draw(number[0]['x'], number[0]['y'],
                        number[0]['w'], number[0]['h'], 75+number[0]['w']/2 +26*i, 559-number[0]['h']/2, 26, 22)

    def top_score(image):
        for i in range (0,6):
            image.clip_draw(number[0]['x'], number[0]['y'],
                        number[0]['w'], number[0]['h'], 426+number[0]['w']/2 +26*i, 128-number[0]['h']/2, 26, 22)

    def coin(image):
        for i in range (0,2):
            image.clip_draw(number[0]['x'], number[0]['y'],
                        number[0]['w'], number[0]['h'], 326+number[0]['w']/2 +26*i, 559-number[0]['h']/2, 26, 22)

    def world(image):
        image.clip_draw(number[1]['x'], number[1]['y'],
                        number[1]['w'], number[1]['h'], 475 + number[1]['w'] / 2, 559 - number[1]['h']/2, 26, 22)
