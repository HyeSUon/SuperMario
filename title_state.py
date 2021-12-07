import game_framework
from pico2d import *
import json
import server
server.name = "TitleState"
image = None
score = None
# 숫자 좌표값 불러오기
with open('json//number.json', 'r') as f:
    number = json.load(f)

def enter():
    global image
    image = load_image('images//Title.png')
    server.score = load_image('images//char.png')

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
    # score.point(server.score)
    # score.top_score(server.score)
    # score.coin(server.score)
    # score.world(server.score)
    update_canvas()

def update():
    pass
def pause():
    pass
def resume():
    pass
