import time
from helpers import Color, int_to_Color, brighten_color, darken_color, blend_colors
from modules import Module
from noise import snoise3
import pygame



class Perlin_rain(Module):

    def __init__(self, screen):
        super(Perlin_rain, self).__init__(screen)

    def _map_to_24bit(self, value):
        """
        maps a 0.0-1.0 value to a 24-bit int

        :param value: 0.0-1.0
        :return: 24 bit int
        """

        return int(max(0, round(value * 16777215)))

    def get_rain_value(self, x, y, t):
        current_color = self.screen.pixel[x][y]
        factor = snoise3(x + 0.5, y + 0.5, t, 4)

        if (factor >= 0):
            return blend_colors(current_color, brighten_color(current_color, factor), 0.5)


        else:
            return blend_colors(current_color, darken_color(current_color, factor), 0.5)

    def draw(self):
        t = time.clock()
        for x in range(16):
            for y in range(16):
                self.screen.pixel[x][y] = self.get_rain_value(x, y, t)

        self.screen.update()

    def tick(self):
        self.draw()

    def on_start(self):
        for x in range(self.screen.width):
            for y in range(self.screen.height):
                self.screen.pixel[x][y] = Color(125, 0, 0)

        self.screen.update()

if __name__ == "__main__":
    from screen.virtualscreen import VirtualScreen

    screen = VirtualScreen()
    perlin = Perlin_rain(screen)
    perlin.start()

    while True:
        pygame.time.wait(10)
        for event in pygame.event.get():
            pass