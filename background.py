import server
from pico2d import *


class Background:

    def __init__(self):
        self.image = load_image('images//World1-1.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.window_left = 0;
        self.window_bottom = 0;
    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom + 600,
                                       server.background.canvas_width, server.background.canvas_height,
                                       0, 0)
        pass

    def update(self):
        if server.mario.dir == 1 and (self.window_left + self.canvas_width//2) < server.mario.x:
            self.window_left = clamp(0, int(server.mario.x) - server.background.canvas_width // 2,
                                     server.background.w - server.background.canvas_width)
        self.window_bottom = clamp(0, int(server.mario.y) - server.background.canvas_height // 2,
                                   server.background.h - server.background.canvas_height)
    def handle_event(self, event):
        pass