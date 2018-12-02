import pygame
import config
from .abstractscreen import AbstractScreen

instance = None

class Screen(AbstractScreen):
	def __init__(self, width = 16, height = 16, led_pin = 18, led_freq_hz = 800000, led_dma = 5, led_invert = False, led_brightness = 200):
		super(Screen, self).__init__(width, height)
		import neopixel
		
		self.strip = neopixel.Adafruit_NeoPixel(width * height, led_pin, led_freq_hz, led_dma, led_invert, led_brightness)
		self.strip.begin()
		self.update_brightness()
		
		global instance
		instance = self	
	
	def update(self):

		for i in range(self.strip.numPixels()):
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

			self.strip.setPixelColor(i, self.pixel[x][y])

			"""
			(0,0) = strip[15]
			(15,0)= strip[0]
			(0,1)= strip[16]
			(15,1)= strip[31]
			(15,15)= strip[255]
			"""



		self.strip.show()

	def update_brightness(self):
		#Exponential brightnes with 9 levels 7-255 in 8-bit terms
		self.strip.setBrightness(int(4 + 3.1 * (config.brightness + 1)**2))

	def set_brightness(self, value):
		value = min(max(value, 0), 8)
		config.brightness = value
		self.update_brightness()
		config.store()

	def get_brightness(self):
		return config.brightness