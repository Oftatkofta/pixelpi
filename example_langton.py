import pygame
from .modules.langtons_ant import LangtonsAnt
from .screenfactory import create_screen
import time
from . import config
from .color_palettes import color_palettes

screen = create_screen()

langtons_ant = LangtonsAnt(screen, rule="RRRRL")
langtons_ant.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)