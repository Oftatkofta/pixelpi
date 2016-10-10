from __future__ import print_function
from helpers import *
from modules import Module
from PIL import Image
import os
import string




class TextScroller(Module):

    def __init__(self, screen, text, fontfile="numbers_font.bmp"):
        super(TextScroller, self).__init__(screen)
        self.text = text
        self.font = self.load_font(fontfile)
        self.position = 0

    def load_font(self, fontfile):

        # Gets the parent directory of the module and appends "/fonts/" + fontfile

        loadme = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "fonts", fontfile)

        font = Image.open(loadme)

        return font

    def draw_letter(self, letter, pos, color, letter_width=3, letter_height=7):
        """
        Crops a letter from the chosen font and draws it at a defined position
        the font is expected to be monospaced with 1 pixel between characters
        and in the same order as in string.printable.

        Raises IndexError if no pixel of letter is visible on screen.

        Args:
        	letter: letter to draw (ASCII)
        	pos: position to draw letter
        	color:
        	letter_width:
        	letter_height:

        Returns:
                None

        """
        if (pos.x+letter_width) < 0 or pos.x > 15:
            raise IndexError("Letter outside screen!")
        if (pos.y-letter_height) < 0 or pos.y > 15:
            raise IndexError("Letter outside screen!")

        index = string.printable.find(letter)

        #Turn all whitespace and non-ascii characters in to space
        if index > 94 or index == -1:
            index = 94

        crop_x = index * (letter_width + 1) + 1
        crop_y = 1

        crop_box = (crop_x, crop_y, crop_x + letter_width+1, letter_height+1)
        letter_img = self.font.crop(crop_box)

        for x in range(letter_img.size[0]):
            for y in range(letter_img.size[1]):
                pixel = letter_img.getpixel((x,y))
                if pixel != (0, 0, 0):
                    try:
                        self.screen.pixel[pos.x + x][pos.y + y] = color
                    except IndexError:
                        #to allow scrolling across the screen
                        pass


    def draw_text(self, color, x_position, y_position=4):


    def draw(self):
        self.screen.clear()
        self.draw_text(Color(255, 255, 255), colon)
        self.screen.update()

    def tick(self):
        self.draw(False)
        time.sleep(0.5)
