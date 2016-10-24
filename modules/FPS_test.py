import datetime
from helpers import *
from modules import Module
from PIL import Image
import os


class FPS(Module):

	def __init__(self, screen, fontfile = "numbers_font.bmp"):
		super(FPS, self).__init__(screen)

		self.fontfile = fontfile

		# Gets the parent directory of the module and appends /fonts +
		# fontfile to it
		loadme = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", fontfile)

		self.number_font = Image.open(loadme)
		self.lastframe = datetime.datetime.now()

	def draw_digit(self, digit, pos, color):
		"""
        Crops a digit from the number font and draws it ar a defined position
        Numberfont is made up of 3x7 digit images spaced with 1 empty pixel row in between.

        :param digit: digit to draw
        :param pos: position to draw digit
        :param color: Color of digit
        :return: None
        """
		box = (digit*4+1, 1, digit*4+4, 8)
		number = self.number_font.crop(box)
		for x in range(number.size[0]):
			for y in range(number.size[1]):
				pixel = number.getpixel((x,y))
				if pixel == (255, 255, 255):
					self.screen.pixel[pos.x + x][pos.y + y] = color

	def draw_FPS(self, color=Color(255,255,255)):

		now = datetime.datetime.now()
		delta_t =  now - self.lastframe
		self.lastframe = now
		fps = str(round(1/delta_t.total_seconds(), 1)).zfill(4)

		self.draw_digit(int(fps[0]), Point(1, 4), color)
		self.draw_digit(int(fps[1]), Point(5, 4), color)
		self.screen.pixel[9][10] = color
		self.draw_digit(int(fps[3]), Point(11, 4), color)

	def draw(self):
		self.screen.clear_pixel()
		self.draw_FPS()
		self.screen.update()

	def tick(self):
		self.draw()
