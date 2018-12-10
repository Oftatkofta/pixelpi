import os
import string
import time

from PIL import Image

from modules import Module
from helpers import Color, Point


class TextScroller(Module):
    #TODO find bug that replaces space with ~
    """
    Scrolls a text across the screen, defaults to a 3x7 pixel font.

    text: An ASCII text
    color: Color of text
    speed: sleeptime between frame updates, lower is faster
    y_position: y position of the top of the text
    fontfile: an image file of the font to be displayed, loaded from pixelpi/fonts/
            It is expected to be monospaced with 1 pixel between characters
            characters should appear in the same order as in string.printable.
    letter_width: width of letters in pixels
    letter_height: height of letters in pixels

    """

    def __init__(self, screen, text, color=Color(255,255,255), speed=0.1, y_position=4,
                 fontfile="3x7_font_printable.bmp", letter_width=3, letter_height=7):

        super(TextScroller, self).__init__(screen)
        self.text = text
        self.color = color
        self.speed = speed
        self.y_position = y_position
        self.font = self.load_font(fontfile)
        self.letter_width = letter_width
        self.letter_height = letter_height

        # Width of text in pixels, incl 1 px padding between letters
        self.textstrip_width = len(self.text)*(self.letter_width + 1)
        self.textstrip_position = -16 #Where the left side of the screen is in relation to the textstrip



    def load_font(self, fontfile):

        # Gets the parent directory of the module and appends "/fonts/" + fontfile

        loadme = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "fonts", fontfile)

        font = Image.open(loadme)

        return font

    def draw_letter(self, letter, pos):
        """
        Crops a letter from the chosen font and draws it at a defined position
        the font is expected to be monospaced with 1 pixel between characters
        and in the same order as in string.printable.

        Raises IndexError if no pixel of letter is visible on screen.

        Args:
        	letter: letter to draw (ASCII)
        	pos: position to draw letter

        Returns:
                None

        """

        if (pos.x + self.letter_width) < 0 or pos.x > 15:
            raise IndexError("Letter outside screen!")
        if (pos.y + self.letter_height) < 0 or pos.y > 15:
            raise IndexError("Letter outside screen!")

        index = string.printable.find(letter)

        #Turn all whitespace and non-ascii characters in to space
        if index > 94 or index == -1:
            index = 95

        if letter == " ":
            index = 95

        crop_x = index * (self.letter_width + 1)
        crop_y = 1

        crop_box = (crop_x, crop_y, crop_x + self.letter_width+1, self.letter_height+1)
        letter_img = self.font.crop(crop_box)

        for x in range(letter_img.size[0]):
            for y in range(letter_img.size[1]):
                pixel = letter_img.getpixel((x,y))
                if pixel != (0, 0, 0):
                    try:
                        self.screen.pixel[pos.x + x][pos.y + y] = self.color
                    except IndexError:
                        #to allow scrolling across the screen
                        pass


    def draw_text(self):
        visible_letters = self.get_visible_letters()
        for l in visible_letters:
            self.draw_letter(l[0], Point(l[1], self.y_position))

    def get_visible_letters(self):
        """

        Returns:
        	a list with tuples(letter, x_position_to_draw_letter)

        """
        out=[]
        last_i = None

        for x in range(self.screen.width):
            pos = self.textstrip_position + x
            if 0 <= pos <= self.textstrip_width:

                i = pos // (self.letter_width + 1)

                #print(pos, i)
                if (last_i != i) and not i > (len(self.text)-1):
                    out.append((self.text[i], x))
                    last_i = i

        return out


    def draw(self):
        self.screen.clear_pixel()
        self.draw_text()
        self.screen.update()

    def tick(self):
        self.draw()
        self.textstrip_position += 1
        if self.textstrip_position > self.textstrip_width:
            self.textstrip_position = -16
            time.sleep(1)
        time.sleep(self.speed)
