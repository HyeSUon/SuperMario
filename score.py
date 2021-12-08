from pico2d import *

import server
import json

with open('json//number.json', 'r') as f:
    number = json.load(f)

image = None

