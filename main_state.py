import random
import json
import os
import title_state

import player

from pico2d import *

import game_framework


name = "MainState"
mario = None

def enter():
    global mario
    mario = player.Mario()

def exit():
    del(mario)
    close_canvas()

def pause():
    pass


def resume():
    pass


def handle_events():
    global mario
    events = get_events()
    for event in events:
        #종료버튼
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
        #좌우이동
            elif event.key == SDLK_RIGHT:
                mario.dir += 1
            elif event.key == SDLK_LEFT:
                mario.dir -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.dir -= 1
            elif event.key == SDLK_LEFT:
                mario.dir += 1


def update():
    mario.update()
    delay(0.01)

def draw():
    clear_canvas()
    mario.draw()
    update_canvas()

