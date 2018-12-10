import time
import datetime
from helpers import Color, Point, binary_to_color
from modules import Module
from PIL import Image
import os


class Clock2(Module):

    def __init__(self, screen, fontfile="numbers_font.bmp", fadetime=1):
        super(Clock2, self).__init__(screen)

        self.fontfile = fontfile
        self.fadetime = fadetime
        # Gets the parent directory of the clock2 module and appends /fonts +
        # fontfile to it
        loadme = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", fontfile)

        self.number_font = Image.open(loadme)

    def draw_digit(self, digit, pos, color):
        """
        Crops a digit from the number font and draws it ar a defined position
        Numberfont is made up of 3x7 digit images spaced with 1 empty pixel row in between.

        :param digit: digit to draw
        :param pos: position to draw digit
        :param color: Color of digit
        :return: None
        """
        box = (digit * 4 + 1, 1, digit * 4 + 4, 8)
        number = self.number_font.crop(box)
        for x in range(number.size[0]):
            for y in range(number.size[1]):
                pixel = number.getpixel((x, y))
                if pixel == (255, 255, 255):
                    self.screen.pixel[pos.x + x][pos.y + y] = color

    def draw_time(self, second=True, binary=True, y_position=0):
        now = datetime.datetime.now()

        self.draw_digit(now.hour // 10, Point(0, y_position), Color(0, 0, 255))
        self.draw_digit(now.hour % 10, Point(4, y_position), Color(0, 0, 255))
        self.draw_digit(now.minute // 10, Point(9, y_position), Color(255, 0, 0))
        self.draw_digit(now.minute % 10, Point(13, y_position), Color(255, 0, 0))

        if second:
            self.draw_digit(now.second // 10, Point(9, y_position + 8), Color(0, 128, 0))
            self.draw_digit(now.second % 10, Point(13, y_position + 8), Color(0, 128, 0))

        if binary:
            binary_hour = bin(now.hour)[2:].zfill(6)
            binary_minute = bin(now.minute)[2:].zfill(6)
            binary_second = bin(now.second)[2:].zfill(6)
            for i in range(6):
                self.screen.pixel[i + 1][9] = binary_to_color(binary_hour[i])
                self.screen.pixel[i + 1][11] = binary_to_color(binary_minute[i])
                self.screen.pixel[i + 1][13] = binary_to_color(binary_second[i])

    # else:
    # 	for s in range(now.second):
    # 		if (s // 4) % 2 == 0:
    # 			self.screen.pixel[s // 4][15 - 2*(s % 8)] = color
    # 		else:
    # 			self.screen.pixel[s // 4][8 + 2*(s % 4)] = color

    def draw(self):
        self.screen.clear_pixel()
        self.draw_time()
        self.screen.update()

    def tick(self):
        self.draw()
        time.sleep(1)

    def on_stop(self):
        if self.fadetime != 0:
            self.screen.fade_out(self.fadetime)
