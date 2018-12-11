import time
import string

import pygame

from screenfactory import create_screen
from modules.text_scroller import TextScroller
from helpers import Color
import config

screen = create_screen()

text = "US20160168579A1 --> TGACGTCGTAACATACTGGCTATAGCTTAGTGCTGATAGGCTATAGGCTAGTTGCGTTCCCTACTGTGATAAATAAGTTAGTGCATTGAG"

scroller = TextScroller(screen, text, color=Color(0, 255, 0), speed=0.1, y_position=9)
scroller.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.1)