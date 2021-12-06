import game_framework
from pico2d import *
from ball import Ball

import game_world



# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

mario_weight = [36, 45, 33, 39, 39, 48, 42, 36, 39, 40, 39, 39, 39, 42]

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE = range(5)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


# Boy States

class IdleState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS

    def exit(boy, event):
        # if event == SPACE:
        #     boy.fire_ball()
        pass

    def do(boy):
        boy.y -= boy.fall_speed * game_framework.frame_time

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(0, 96*2, 48, 36, boy.x, boy.y)
        else:
            boy.image.clip_composite_draw(0, 96*2, 48, 36, 3.141592, 'v', boy.x, boy.y, 48, 36)


class RunState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        boy.dir = clamp(-1, boy.velocity, 1)

    def exit(boy, event):
        # if event == SPACE:
        #     boy.fire_ball()
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)
        boy.y -= boy.fall_speed * game_framework.frame_time

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame + 1) * 48, 96*2, 48, 36, boy.x, boy.y)
        else:
            boy.image.clip_composite_draw(int(boy.frame+1) * 48, 96*2, 48, 36, 3.141592,'v', boy.x, boy.y, 48, 36)
class JumpState:
    jumping = 120
    jump_velocity = 1
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        if boy.velocity != 0:
            boy.dir = clamp(-1, boy.velocity, 1)
        if event == SPACE:
            boy.fall_speed = 1
    def exit(boy, event):
        pass
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(48*5, 96 * 2, 48, 36, boy.x, boy.y)
        else:
            boy.image.clip_composite_draw(48*5, 96 * 2, 48, 36, 3.141592, 'v', boy.x, boy.y, 48, 36)

    def do(boy):
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)
        boy.y -= boy.fall_speed * game_framework.frame_time
        MAX_Y = boy.y + JumpState.jumping
        if boy.y <= MAX_Y:
            boy.y += JumpState.jump_velocity + game_framework.frame_time

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE: JumpState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, SPACE: JumpState},
    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState, SPACE: JumpState}
}

class Boy:

    def __init__(self):
        self.x, self.y = 300, 90 + 100
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('images\mario.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.velocity = 0
        self.acceleration = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.fall_speed = 1
    def get_bb(self):
        if self.cur_state == IdleState:
            return self.x - 18, self.y - 18, self.x + 18, self.y + 18
        if self.cur_state == RunState:
            return self.x - mario_weight[int(self.frame + 1)] / 2,self.y - 18, self.x + mario_weight[int(self.frame + 1)] / 2, self.y + 18
        if self.cur_state == JumpState:
            return self.x - mario_weight[5]/2, self.y - 18, self.x+mario_weight[5]/2, self.y+18
        return 0, 0, 0, 0


    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir * RUN_SPEED_PPS * 10)
        game_world.add_object(ball, 1)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
    def stop(self):
        self.fall_speed = 0

