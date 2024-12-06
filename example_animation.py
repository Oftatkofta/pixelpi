from screenfactory import create_screen
from modules.animation import Animation, CropAnimation
import config
import pygame
import time

screen = create_screen()

animation = CropAnimation(screen, "animations/crypto")
while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)