import game_framework
import pico2d
import option
import start_state
import main_state
pico2d.open_canvas(option.CANVAS_WIDTH, option.CANVAS_HEIGHT)
game_framework.run(main_state)
pico2d.close_canvas()