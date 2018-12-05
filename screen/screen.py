import config
from screen import AbstractScreen
import board
import neopixel

instance = None

class Screen(AbstractScreen):
	def __init__(self, width = 16, height = 16, pixel_pin = board.D18, brightness = 0.1, auto_write = False):
		super(Screen, self).__init__(width, height)
		self.numPixels = width * height

		self.strip = neopixel.NeoPixel(pixel_pin, self.numPixels, brightness=brightness, auto_write=auto_write, pixel_order=neopixel.GRB)
		#self.strip.begin()
		#TODO: fix brightness setting
		#self.update_brightness()

		global instance
		instance = self

	def update(self):

		for i in range(self.numPixels):
			# find the x/y coordinates with modulo and floor division
			if (i//16) % 2 == 0:
				#even rows
				x = 15 - (i % self.width)
				y = i // self.height

			else:
				#odd rows
				x = i % self.width
				y = i // self.height

			# get and set the RGB values from the pixel in question

			self.strip[i] = self.pixel[x][y]

			"""
			(0,0) = strip[15]
			(15,0)= strip[0]
			(0,1)= strip[16]
			(15,1)= strip[31]
			(15,15)= strip[255]
			"""

		self.strip.show()

	def update_brightness(self):
		#Linear brightnes set with float 0.-1.0
		self.strip.brightness(float(config.brightness))

	def set_brightness(self, value):
		value = min(max(value, 0.0), 1.0)
		config.brightness = value
		self.update_brightness()
		config.store()

	def get_brightness(self):
		return config.brightness