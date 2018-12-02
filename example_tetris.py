from .screenfactory import create_screen
from .modules.tetris import *
import time
from . import config
from . import input

screen = create_screen()

tetris = Tetris(screen)
while True:
	pygame.time.wait(10)
	input.tick()