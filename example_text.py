import time
import string

from screenfactory import create_screen
from modules.text_scroller import TextScroller
from helpers import Color
import config

if config.virtual_hardware:
	import pygame

screen = create_screen()

text = "abcdef"

scroller = TextScroller(screen, text, color=Color(0, 255, 0), speed=0.1, y_position=4)
scroller.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.1)