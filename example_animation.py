from .screenfactory import create_screen
from .modules.animation import *
from . import config

screen = create_screen()

animation = Animation(screen, "animations/punksprite")
while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)