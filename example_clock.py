from .screenfactory import create_screen
from .modules.clock2 import Clock2
from . import config
import time
import pygame

screen = create_screen()

clock = Clock2(screen)
clock.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)