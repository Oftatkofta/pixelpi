from helpers import Color, RGBColor, int_to_rgb_color, rgb_tuple_to_int, darken_color
import time
from PIL import Image

class AbstractScreen(object):
    """
    Abstract base class for a screen or display, providing a framework for
    managing and manipulating a matrix of pixels and a staging image for complex
    image operations.
    """
    def __init__(self, width = 16, height = 16):
        """
        Initializes the screen with the given dimensions.
        
        :param width: The width of the screen in pixels.
        :param height: The height of the screen in pixels.
        """
        self.width = width
        self.height = height

        #Pixels to shift out to the strip stored as int
        self.pixel = [[Color(0,0,0) for y in range(height)] for x in range(width)]

        #A PIL-Image object to use for complex image manipulations
        self.stage = Image.new("RGB", (width, height))


    def clear_pixel(self, color = Color(0, 0, 0)):
        """
        Clears the pixel matrix by setting all pixels to the specified color.
        
        :param color: The color to set all pixels to (default is black).
        """
        for x in range(self.width):
            for y in range(self.height):
                self.pixel[x][y] = color

    def clear_stage(self):
        """
        Clears the staging image by creating a new image with the screen's dimensions.
        """
        self.stage = Image.new("RGB", (self.width, self.height))

    def stage_to_pixels(self):
        """
        Transfers the staged image to the pixel matrix by converting each pixel of the
        image to an integer representation and updating the pixel matrix.
        """
        #moves the pixels from the staging image to self.pixel
        for x in range(self.width):
            for y in range(self.height):
                px = rgb_tuple_to_int(self.stage.getpixel((x,y)))
                self.pixel[x][y] = px

    def update(self):
        """
        Placeholder method for updating the display. This should be implemented by Screen subclasses.
        """
        pass

    def fade(self, duration, fadein):
        """
        Performs a fade in or fade out animation over the specified duration.
        
        :param duration: The duration of the fade effect in seconds.
        :param fadein: A boolean indicating whether to fade in (True) or out (False).
        """
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
        """
        Initiates a fade-in effect from black to the current image over the given duration.
        
        :param duration: The duration of the fade-in effect in seconds (default is 0.5).
        """
        self.fade(duration, True)

    def fade_out(self, duration=0.5):
        """
        Initiates a fade-out effect from the current image to black over the given duration.
        
        :param duration: The duration of the fade-out effect in seconds (default is 0.5).
        """
        self.fade(duration, False)

    def get_colorlist(self):
        """
        Retrieves a list of unique RGB colors currently displayed on the screen.
        
        :return: A list of unique Color objects in the pixel matrix.
        """
        out = []
        for x in range(self.width):
            for y in range(self.height):
                pixel = self.pixel[x][y]

                if pixel not in out:
                    out.append(pixel)

        return out
