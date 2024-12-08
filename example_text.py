import time
import string

from screenfactory import create_screen
from modules.text_scroller import TextScroller
from helpers import Color
import config

if config.virtual_hardware:
	import pygame

screen = create_screen()

text = "In a hole in the ground, there lived a Hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort."

scroller = TextScroller(screen, text, color=Color(0, 255, 0), speed=0.1, y_position=4)
scroller.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.1)