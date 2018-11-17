import pygame
from modules.langtons_ant import LangtonsAnt
from screenfactory import create_screen
import time
import config
from color_palettes import *

screen = create_screen()

langtons_ant = LangtonsAnt(screen, rule="RL", colorlist=color_palettes.colorcombo210())
langtons_ant.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)