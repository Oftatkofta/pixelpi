import time
import math
from helpers import *
from modules import Module

class FPS(Module):
	def __init__(self, screen):
		super(FPS, self).__init__(screen)
	
	def draw(self):
		self.screen.clear_pixel()
		for x in range(16):
			for y in range(16):
				self.screen.pixel[x][y] = Color(0,255,255)
				self.screen.update()
				#time.sleep(0.1)
		#self.screen.update()


	def tick(self):
		self.draw()
		#time.sleep(0.1)