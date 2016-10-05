import collections
import random
import time
import datetime
import os
import math
from helpers import *
from modules import Module
from PIL import Image
import os

fontfile = "numbers_font.bmp"

#Gets the parent directory of the clock2 module and appends /fonts + fontfile to it
loadme = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "fonts", fontfile)

number_font = Image.open(loadme)

class Clock2(Module):
    def __init__(self, screen):
        super(Clock2, self).__init__(screen)

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
        number = number_font.crop(box)
        for x in range(number.size[0]):
            for y in range(number.size[1]):
                pixel = number.getpixel((x,y))
                if pixel == (255, 255, 255):
                    self.screen.pixel[pos.x + x][pos.y + y] = color


    def draw_time(self, color, second=True, y_position=0):
        now = datetime.datetime.now()

        self.draw_digit(now.hour // 10, Point(0, y_position), color)
        self.draw_digit(now.hour % 10, Point(4, y_position), color)
        self.draw_digit(now.minute // 10, Point(9, y_position), color)
        self.draw_digit(now.minute % 10, Point(13, y_position), color)

        if second:
            self.draw_digit(now.second // 10, Point(9, y_position+8), color)
            self.draw_digit(now.second % 10, Point(13, y_position+8), color)

        else:
            for s in range(now.second):
                if (s // 4) % 2 == 0:
                    self.screen.pixel[s // 4][
                        15 - 2*(s % 8)] = color
                else:
                    self.screen.pixel[s // 4][
                        8 + 2*(s % 4)] = color

    def draw(self, colon=True):
        self.screen.clear()
        self.draw_time(Color(255, 255, 255), colon)
        self.screen.update()

    def tick(self):
        self.draw(False)
        time.sleep(0.5)
        self.draw(False)
        time.sleep(0.5)
