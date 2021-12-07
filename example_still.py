from screenfactory import create_screen
from modules.still_image import StillImage
import config
import time

if config.virtual_hardware:
	import pygame

screen = create_screen()

gallery = StillImage(screen, "_crypto/first_clue.gif")
gallery.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)