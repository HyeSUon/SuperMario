import random
import json
import os
import title_state
from pico2d import *

import game_framework



name = "MainState"


def enter():
    open_canvas()


def exit():
    close_canvas()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                pause()


def update():
    pass


def draw():
    pass


