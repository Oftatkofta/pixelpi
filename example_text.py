from screenfactory import create_screen
from modules.text_scroller import TextScroller
import config
import time
import pygame
import string

screen = create_screen()

text="Hello world, you are... sometimes cruel!"

scroller = TextScroller(screen, string.printable)
scroller.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)