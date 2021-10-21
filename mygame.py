import game_framework
import pico2d
import option
import start_state

pico2d.open_canvas(option.CANVAS_WIDTH, option.CANVAS_HEIGHT)
game_framework.run(start_state)
pico2d.close_canvas()