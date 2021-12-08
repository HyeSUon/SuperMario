import game_framework
import pico2d
import title_state

import server

pico2d.open_canvas(800, 600)
game_framework.run(title_state)
pico2d.close_canvas()