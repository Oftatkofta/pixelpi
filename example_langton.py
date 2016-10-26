import pygame
from modules.langtons_ant import LangtonsAnt
from screenfactory import create_screen
import time
import config

screen = create_screen()

langtons_ant = LangtonsAnt(screen)
langtons_ant.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.001)