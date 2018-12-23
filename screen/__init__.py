from helpers import Color, RGBColor, int_to_rgb_color, rgb_tuple_to_int, darken_color
import time
from PIL import Image

class AbstractScreen(object):
    def __init__(self, width = 16, height = 16):
        self.width = width
        self.height = height

        #Pixels to shift out to the strip stored as int
        self.pixel = [[Color(0,0,0) for y in range(height)] for x in range(width)]

        #A PIL-Image object to use for complex image manipulations
        self.stage = Image.new("RGB", (width, height))


    def clear_pixel(self, color = Color(0, 0, 0)):
        for x in range(self.width):
            for y in range(self.height):
                self.pixel[x][y] = color

    def clear_stage(self):
        self.stage = Image.new("RGB", (self.width, self.height))

    def stage(self):
        #moves the pixels from the staging image to self.pixel
        for x in range(self.width):
            for y in range(self.height):
                px = rgb_tuple_to_int(self.stage.getpixel((x,y)))
                self.pixel[x][y] = px

    def update(self):
        pass

    def fade(self, duration, fadein):
        frame = [[self.pixel[x][y] for y in range(self.height)] for x in range(self.width)]

        start = time.time()
        end = start + duration

        while time.time() < end:
            progress = (time.time() - start) / duration
            if not fadein:
                progress = 1.0 - progress
            self.pixel = [[darken_color(frame[x][y], progress) for y in range(self.height)] for x in range(self.width)]
            self.update()

    def fade_in(self, duration=0.5):
        self.fade(duration, True)

    def fade_out(self, duration=0.5):
        self.fade(duration, False)

    def get_colorlist(self):
        """
        Returns a list of the unique RGB colors in the currently displayed image

        :return: (list) unique Color objects in self.pixel
        """

        out = []
        for x in range(self.width):
            for y in range(self.height):
                pixel = self.pixel[x][y]

                if pixel not in out:
                    out.append(pixel)

        return out
