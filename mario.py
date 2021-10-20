from pico2d import *
import random
import C
class Background:
    def __init__(self):
        self.image = load_image('1stage.png')
    def draw(self):
        self.image.draw(400, 300)
class Gravity:
    def __init__(self):
        self.g = 5
    def update(self):
        monster.y -= self.g
        mario.y -= self.g
        mushroom.y -= self.g
class Board:
    def __init__(self):
        self.image = load_image('image\items.png')
        self.x, self.y = 0, 100

    def get_num_x(self, x):
        self.x = x
    def get_num_y(self, y):
        self.y = y
    def update(self):
        #마리오 충돌 처리
        if (mario.x - self.x) ** 2 < ((C.MARIO_WIDTH + C.BOARD_WIDTH) / 2) ** 2 \
                and (mario.y - self.y) ** 2 < ((C.MARIO_HEIGHT + C.BOARD_HEIGHT) / 2) ** 2:
            mario.y += 5
        #몬스터 충돌 처리
        if (monster.x - self.x) ** 2 < ((C.MONSTER_WIDTH + C.BOARD_WIDTH) / 2) ** 2 \
                and (monster.y - self.y) ** 2 < ((C.MONSTER_HEIGHT + C.BOARD_HEIGHT) / 2) ** 2:
            monster.y += 5
        #버섯 충돌 처리
        if (mushroom.x - self.x) ** 2 < ((C.MUSHROOM_WIDTH + C.BOARD_WIDTH) / 2) ** 2 \
                and (mushroom.y - self.y) ** 2 < ((C.MUSHROOM_HEIGHT + C.BOARD_HEIGHT) / 2) ** 2:
            mushroom.y += 5
    def draw(self):
        self.image.clip_draw(63, 114-44, C.BOARD_WIDTH, C.BOARD_HEIGHT, self.x, self.y)

class Monster:
    def __init__(self):
        self.image = load_image('image\character_kit.gif')
        self.x, self.y = 400, 150
        self.dir = -1
        self.exist = True
    def update(self):
        #마리오와 충돌처리
        if self.exist == True and mario.miracle == False:
            if (mario.x - self.x) ** 2 < ((C.MARIO_WIDTH + C.MONSTER_WIDTH) / 2) ** 2 \
                and (mario.y - self.y) ** 2 < ((C.MARIO_HEIGHT + C.MONSTER_HEIGHT) / 2) ** 2:
                if mario.big == True:
                    mario.big = False
                    mario.y -= (C.BIG_MARIO_HEIGHT - C.MARIO_HEIGHT) / 2
                    mario.miracle = True
                else:
                    mario.gameover = True
    def draw(self):
        if self.exist == True:
            if self.dir > 0:
                self.image.clip_draw(8, 650 - 402, C.MONSTER_WIDTH, C.MONSTER_HEIGHT, self.x, self.y)
            else:
                self.image.clip_draw(38, 650 - 402, C.MONSTER_WIDTH, C.MONSTER_HEIGHT, self.x, self.y)

class Mushroom:
    def __init__(self):
        self.image = load_image('image\items.png')
        self.x, self.y = 300, 150
        self.exist = True
    def update(self):
        if self.exist == True:
            #마리오와 충돌 체크
            if (mario.x - self.x)**2 < ((C.MARIO_WIDTH+C.MUSHROOM_WIDTH)/4)**2 \
                    and (mario.y - self.y)**2 < ((C.MARIO_HEIGHT+C.MUSHROOM_HEIGHT)/4)**2:
                if mario.big == False:
                    mario.y += (C.BIG_MARIO_HEIGHT - C.MARIO_HEIGHT) / 2
                self.exist = False
                mario.big = True
            self.x += 1
    def  draw(self):
        if self.exist == True:
            self.image.clip_draw(184, 114 - 50, C.MUSHROOM_WIDTH, C.MUSHROOM_HEIGHT, self.x, self.y)

class Mario:
    def __init__(self):
        self.image = load_image('image\character_kit.gif')
        self.x, self.y = 100, 150
        self.frame = 0
        self.frameNumber = 0
        self.big = False
        self.dir = 0
        self.old_dir = 1
        self.gameover = False
        self.miracle = False
        self.miracle_count = C.MIRACLE_COUNT #30 = 1초 무적 정도
        self.jump = 0
    def update(self):
        self.x += self.dir * 10
        self.y += self.jump * 10
        if self.dir > 0 or self.dir < 0:
            self.frameNumber = 3
        elif self.dir == 0:
            self.frameNumber = 1

        self.frame = (self.frame + 1) % self.frameNumber
        #무적 구현
        if self.miracle == True:
            self.miracle_count -= 1
            if self.miracle_count == 0:
                self.miracle = False
                self.miracle_count = C.MIRACLE_COUNT
    def draw(self):
        if self.big == True:
            # 좌우걷기
            if self.dir > 0:
                self.image.clip_draw(215 + self.frame * 30, 650 - 118, C.BIG_MARIO_WIDTH, C.BIG_MARIO_HEIGHT, self.x, self.y)
            elif self.dir < 0:
                self.image.clip_draw(6 + self.frame * 30, 650 - 156, C.BIG_MARIO_WIDTH, C.BIG_MARIO_HEIGHT, self.x, self.y)
            # 멈췄을 때 모션
            elif self.dir == 0:
                if self.old_dir > 0:
                    self.image.clip_draw(185 + self.frame * 30, 650 - 118, C.BIG_MARIO_WIDTH, C.BIG_MARIO_HEIGHT, self.x, self.y)
                else:
                    self.image.clip_draw(96 + self.frame * 30, 650 - 155, C.BIG_MARIO_WIDTH, C.BIG_MARIO_HEIGHT, self.x,self.y)
        if self.big != True:
            #게임오버 모션
            if self.gameover == True:
                self.image.clip_draw(216, 650 - 51, C.MARIO_WIDTH, C.MARIO_HEIGHT, self.x, self.y)
            #좌우걷기
            elif self.dir > 0:
                self.image.clip_draw(216 + self.frame*30, 650 - 51, C.MARIO_WIDTH, C.MARIO_HEIGHT, self.x, self.y)
            elif self.dir < 0:
                self.image.clip_draw(7 + self.frame * 30, 650 - 76, C.MARIO_WIDTH, C.MARIO_HEIGHT, self.x, self.y)
            # 멈췄을 때 모션
            if self.dir == 0:
                if self.old_dir > 0:
                    self.image.clip_draw(186 + self.frame * 30, 650 - 51, C.MARIO_WIDTH, C.MARIO_HEIGHT, self.x, self.y)
                else:
                    self.image.clip_draw(156 + self.frame * 30, 650 - 51, C.MUSHROOM_WIDTH, C.MARIO_HEIGHT, self.x, self.y)

def handle_events():
    global running
    global dir
    global old_dir
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                mario.dir += 1
            elif event.key == SDLK_LEFT:
                mario.dir -= 1
            elif event.key == SDLK_UP:
                mario.jump += 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.dir -= 1
            elif event.key == SDLK_LEFT:
                mario.dir += 1
            elif event.key == SDLK_UP:
                mario.jump -= 1
        if mario.dir != 0:
            mario.old_dir = mario.dir

# initialization code
open_canvas()
background = Background()
mario = Mario()
mushroom = Mushroom()
monster = Monster()
grass =[Board() for i in range(10)]
grass2 =[Board() for i in range(17)]
gravity = Gravity()
running = True
i = 1; j= 1 #임시, 나중에 지울 것 (수정)
grass_count = 0
#game main loop code
while running:
    handle_events()

    #game logic
    if mario.gameover == False:
        mario.update()
        mushroom.update()
        monster.update()
        gravity.update()
        for board in grass:
            board.update()
        for board in grass2:
            board.update()
    else:
        mario.y -= 1
    #game drawing
    clear_canvas()
    background.draw()
    mario.draw()
    mushroom.draw()
    monster.draw()
    for board in grass: #나중에 수정 (자원 낭비)
        board.get_num_x(i*96)
        board.draw()
        i = (i + 1) % 10
    for board in grass2:
        board.y = 50
        board.get_num_x(i*48)
        board.draw()
        i = (i+1)%17
    update_canvas()
    delay(0.01)
