import game_framework
from pico2d import *
import json
import server
name = "TitleState"
image = None
# 숫자 좌표값 불러오기
with open('json//number.json', 'r') as f:
    number = json.load(f)


def enter():
    global image
    image = load_image('images//Title.png')
def exit():
    global image
    del(image)
import main_state

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)
def draw():
    clear_canvas()
    image.draw(400, 300)
    # for i in range (0,6):
    #     score.clip_draw(number[0]['x'], number[0]['y'],
    #                 number[0]['w'], number[0]['h'], 75+number[0]['w']/2 +26*i, 559-number[0]['h']/2, 26, 22)
    # for i in range (0,6):
    #     score.clip_draw(number[0]['x'], number[0]['y'],
    #                 number[0]['w'], number[0]['h'], 426+number[0]['w']/2 +26*i, 128-number[0]['h']/2, 26, 22)
    # for i in range (0,2):
    #     score.clip_draw(number[0]['x'], number[0]['y'],
    #                 number[0]['w'], number[0]['h'], 326+number[0]['w']/2 +26*i, 559-number[0]['h']/2, 26, 22)
    #
    # score.clip_draw(number[1]['x'], number[1]['y'],
    #                 number[1]['w'], number[1]['h'], 475 + number[1]['w'] / 2, 559 - number[1]['h']/2, 26, 22)

    update_canvas()

def update():
    server.score.st(name)
    pass
def pause():
    pass
def resume():
    pass
