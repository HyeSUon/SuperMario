import game_framework
from pico2d import *
import json
import server
import collision
with open('json//character.json', 'r') as f:
    mario_weight = json.load(f)


# Run Speed

PIXEL_PER_METER = (10.0 / 0.2) #10 pixel 20 cm
RUN_SPEED_KMPH = 20.0 #Km/Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 0.25
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

# Mario Event
RIGHTKEY_DOWN, LEFTKEY_DOWN, UPKEY_DOWN, DOWNKEY_DOWN, RIGHTKEY_UP, LEFTKEY_UP, UPKEY_UP, DOWNKEY_UP, SPACE = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UPKEY_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWNKEY_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHTKEY_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFTKEY_UP,
    (SDL_KEYUP, SDLK_UP): UPKEY_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWNKEY_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
}

# Mario State

class IdleState:
    def enter(mario, event):
        if event == RIGHTKEY_DOWN:
            mario.x_velocity += RUN_SPEED_PPS
        elif event == LEFTKEY_DOWN:
            mario.x_velocity -= RUN_SPEED_PPS
        elif event == RIGHTKEY_UP:
            mario.x_velocity -= RUN_SPEED_PPS
        elif event == LEFTKEY_UP:
            mario.x_velocity += RUN_SPEED_PPS

    def do(mario):
        pass

    def exit(mario, event):
        if event== SPACE:
            mario.fire_ball()

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(0, 96*2, 48, 36, mario.cx, mario.cy, 48, 36)
        else:
            mario.image.clip_composite_draw(0, 96*2, 48, 36, 3.141592, 'v', mario.cx, mario.cy, 48, 36)

class RunState:

    def enter(mario, event):
        if event == RIGHTKEY_DOWN:
            mario.x_velocity += RUN_SPEED_PPS
        elif event == LEFTKEY_DOWN:
            mario.x_velocity -= RUN_SPEED_PPS
        elif event == RIGHTKEY_UP:
            mario.x_velocity -= RUN_SPEED_PPS
        elif event == LEFTKEY_UP:
            mario.x_velocity += RUN_SPEED_PPS
        mario.dir = clamp(-1, mario.x_velocity, 1)

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        mario.x += mario.x_velocity * game_framework.frame_time

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame + 1) * 48, 96*2, 48, 36, mario.cx, mario.cy, 48, 36)
        else:
            mario.image.clip_composite_draw(int(mario.frame+1) * 48, 96*2, 48, 36, 3.141592,'v', mario.cx, mario.cy, 48, 36)


next_state_table = {
    IdleState: {RIGHTKEY_UP: RunState, LEFTKEY_UP: RunState,
                RIGHTKEY_DOWN: RunState, LEFTKEY_DOWN: RunState, SPACE: IdleState},
    RunState: {RIGHTKEY_UP: IdleState, LEFTKEY_UP: IdleState, LEFTKEY_DOWN: IdleState,
               RIGHTKEY_DOWN: IdleState, SPACE: RunState},
}

class Mario:

    def __init__(self, x = 300, y = 50):
        self.x, self.y = x, y
        self.cx, self.cy = 0, 0
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('images\mario.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.x_velocity = 0
        self.y_velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.cur_size = "small"
        self.parent = None
        self.fall_speed = 1
    def get_bb(self):
        if self.cur_state == IdleState:
            return self.cx - 18, self.cy - 18, self.cx + 18, self.cy + 18
        if self.cur_state == RunState:
            return self.cx - mario_weight[self.cur_size][int(self.frame + 1)] / 2,self.y - 18, self.cx + mario_weight[self.cur_size][int(self.frame + 1)] / 2, self.cy + 18
        return 0, 0, 0, 0


    def fire_ball(self):
        # ball = Ball(self.x, self.y, self.dir * RUN_SPEED_PPS * 10)
        # game_world.add_object(ball, 1)
        pass


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        self.x = clamp(server.background.window_left, self.x, server.background.w-1)
        self.y = clamp(0, self.y - self.fall_speed, server.background.h-1)
        self.cx, self.cy = self.x - server.background.window_left, self.y - server.background.window_bottom

        if collision.collide(self, server.grass):
            self.set_parent(server.grass)
            print("mario - grass collide")
    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2
    def set_parent(self, grass):
        self.parent = grass
        self.y = grass.top + 19