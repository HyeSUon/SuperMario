import game_framework
import pico2d

import main_state

pico2d.open_canvas(960, 600)
game_framework.run(main_state)
pico2d.close_canvas()