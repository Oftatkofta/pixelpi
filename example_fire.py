from .screenfactory import create_screen
from .modules.fire import Fire
from . import config
import time
import pygame

screen = create_screen()

fire = Fire(screen)
fire.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)