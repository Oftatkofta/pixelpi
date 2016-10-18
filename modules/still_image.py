from __future__ import print_function
from animation import *
import time
from os import listdir
from helpers import Color, rgb_tuple_to_int
from PIL import Image
from random import shuffle

class StillImage(Module):
	def __init__(self, screen, filename, fadetime = 1):
		super(StillImage, self).__init__(screen)

		self.filename = filename
		self.fadetime = fadetime

		try:
			image = Image.open(self.filename)
		except Exception:
			print('Error loading ' + self.filename)
			raise

		if image.size != (16,16):
			print("resizing:", self.filename)
			image = image.resize((16,16), resample=Image.LANCZOS)

		if image.mode != "RGB":
			# avoid alpha channel and binary image troubles for now
			print("converting:", self.filename, image.mode)
			image = image.convert("RGB")


		self.pixels = [[rgb_tuple_to_int(image.getpixel((x, y))) for y in range(16)] for x in range(16)]

	def draw(self):
		self.screen.pixel = self.pixels

		if self.fadetime != 0:
			self.screen.fade_in(self.fadetime)
		else:
			self.screen.update()

	def tick(self):
		time.sleep(0.1)

	def on_start(self):
		self.draw()

	def on_stop(self):
		if self.fadetime != 0:
			self.screen.fade_out(self.fadetime)