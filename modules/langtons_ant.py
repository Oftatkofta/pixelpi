import time
from helpers import *
from modules import Module
from PIL import Image
import os


class LangtonsAnt(Module):
	"""
	On light turn right, on dark turn left
	"""

	def __init__(self, screen, start_position = Point(7,7), antcolor=Color(255, 0, 0)):
		super(LangtonsAnt, self).__init__(screen)

		self.position = start_position
		self.previous_position = None
		self.antcolor = antcolor
		self.screen.clear_pixel(color=Color(255,255,255))

	def get_pixel_color(self, point):
		return int_to_rgb_color(self.screen.pixel[point.x][point.y])

	def get_direction(self):
		"""
		Calculates the current travelling direction as a "point vector"

		:return:
				a string: "right", "left", "up" or "down"

		"""
		if self.previous_position == None:
			return "up"

		d_x = self.position.x - self.previous_position.x
		d_y = self.position.y - self.previous_position.y

		if (d_x == 1) or (d_x == -15):
			return "right"

		if (d_x == -1) or (d_x == 15):
			return "left"

		if (d_y == 1) or (d_y == -15):
			return "down"

		else:
			return "up"

	def turn_left(self):
		dir = self.get_direction()
		self.previous_position = self.position

		if dir == "up":
			self.position = Point((self.position.x-1)%16, self.position.y)

		if dir == "down":
			self.position = Point((self.position.x+1)%16, self.position.y)

		if dir == "left":
			self.position = Point(self.position.x, (self.position.y-1)%16)

		if dir == "right":
			self.position = Point(self.position.x, (self.position.y+1)%16)

	def turn_right(self):
		dir = self.get_direction()
		self.previous_position = self.position

		if dir == "up":
			self.position = Point((self.position.x+1)%16, self.position.y)

		if dir == "down":
			self.position = Point((self.position.x-1)%16, self.position.y)

		if dir == "left":
			self.position = Point(self.position.x, (self.position.y+1)%16)

		if dir == "right":
			self.position = Point(self.position.x, (self.position.y-1)%16)

	def flip_color(self):
		point = self.position
		c = self.get_pixel_color(point)

		if c == (0, 0, 0):
			self.screen.pixel[point.x][point.y] = Color(255, 255, 255)

		if c == (255, 255, 255):
			self.screen.pixel[point.x][point.y] = Color(0, 0, 0)

	def step(self):
		#print(self.get_direction())
		c = self.get_pixel_color(self.position)
		self.flip_color()
		self.screen.update()

		if c == (0, 0, 0):
			self.turn_left()
		if c == (255, 255, 255):
			self.turn_right()


	def blink(self, ntimes=1):

		pixel_color = self.screen.pixel[self.position.x][self.position.y]

		for i in range(ntimes):
			self.screen.pixel[self.position.x][self.position.y] = self.antcolor
			self.screen.update()
			time.sleep(0.01)
			self.screen.pixel[self.position.x][self.position.y] = pixel_color
			self.screen.update()
			time.sleep(0.01)


	def tick(self):
		self.blink()
		self.step()
		#self.blink()