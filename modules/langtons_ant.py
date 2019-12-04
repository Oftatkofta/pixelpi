import random
import time

from helpers import Color, Point
from modules import Module
from itertools import cycle
from color_palettes import color_palettes



class LangtonsAnt(Module):
    """
    Implemets Langton's ant on a toroidal grid (top-bottom, left-right wrapping)

    The rules are:
    On white turn right, on black turn left, flip the color of the square
    """

    def __init__(self, screen, start_position=Point(random.randint(0, 15), random.randint(0, 15)),
                 antcolor=Color(255, 0, 0), rule="RLLRL", colorlist=color_palettes.firenze(),
                 clear_screen=True):

        super(LangtonsAnt, self).__init__(screen)

        self.position = start_position
        self.previous_position = None
        self.antcolor = antcolor

        self.rule = list(rule)
        self.colors = colorlist[:len(self.rule)] #one turn per color

        # cycle the colors
        self.color_cycle = cycle(self.colors)

        if not clear_screen:
            """
            If we don't clear the screen we need to make sure that there is a turn associated with each
            color used so the ant has a rule for each color it may encounter.
            """
            self.colors = self.screen.get_colorlist()
            print(self.colors)
            rule_generator = cycle(self.rule)
            while len(self.colors) > len(self.rule):
                self.rule.append(next(rule_generator))
        else:
            self.screen.clear_pixel(next(self.color_cycle))

        print(self.rule)
        next(self.color_cycle) #start the cycle

        #rulebook is a dict with color:(L/R, next_color)
        self.rulebook = dict(list(zip(self.colors,
                                 list(zip(self.rule, self.color_cycle)))))

    def get_pixel_color(self, point):
        return self.screen.pixel[point.x][point.y]

    def get_direction(self):
        """
        Calculates the current travelling direction as a "point vector"

        :return:
                a string: "right", "left", "up" or "down"

        """
        if self.previous_position == None:
            return "up"

        d_x = self.position.x - self.previous_position.x
        d_y = self.position.y - self.previous_position.y

        if (d_x == 1) or (d_x == -15):
            return "right"

        if (d_x == -1) or (d_x == 15):
            return "left"

        if (d_y == 1) or (d_y == -15):
            return "down"

        else:
            return "up"

    def turn_left(self):
        dir = self.get_direction()
        self.previous_position = self.position

        if dir == "up":
            self.position = Point((self.position.x - 1) % 16, self.position.y)

        if dir == "down":
            self.position = Point((self.position.x + 1) % 16, self.position.y)

        if dir == "left":
            self.position = Point(self.position.x, (self.position.y - 1) % 16)

        if dir == "right":
            self.position = Point(self.position.x, (self.position.y + 1) % 16)

    def turn_right(self):
        dir = self.get_direction()
        self.previous_position = self.position

        if dir == "up":
            self.position = Point((self.position.x + 1) % 16, self.position.y)

        if dir == "down":
            self.position = Point((self.position.x - 1) % 16, self.position.y)

        if dir == "left":
            self.position = Point(self.position.x, (self.position.y + 1) % 16)

        if dir == "right":
            self.position = Point(self.position.x, (self.position.y - 1) % 16)

    def go_straight(self):
        dir = self.get_direction()
        self.previous_position = self.position

        if dir == "up":
            self.position = Point(self.position.x, (self.position.y + 1) % 16)

        if dir == "down":
            self.position = Point(self.position.x, (self.position.y - 1) % 16)

        if dir == "left":
            self.position = Point((self.position.x - 1) % 16, self.position.y)

        if dir == "right":
            self.position = Point((self.position.x + 1) % 16, self.position.y - 1)

    def flip_color(self):
        point = self.position
        c = self.get_pixel_color(point)

        if c == (0, 0, 0):
            self.screen.pixel[point.x][point.y] = Color(255, 255, 255)

        if c == (255, 255, 255):
            self.screen.pixel[point.x][point.y] = Color(0, 0, 0)

    def flip_current_pixel_color(self, color):
        point = self.position
        self.screen.pixel[point.x][point.y] = color

    def step(self):

        c = self.get_pixel_color(self.position)
        turn = self.rulebook[c][0]
        next_color = self.rulebook[c][1]
        self.flip_current_pixel_color(next_color)
        self.screen.update()

        if turn == "L":
            self.turn_left()
        elif turn == "R":
            self.turn_right()
        else:
            self.go_straight()

    def blink(self, ntimes=1):

        pixel_color = self.screen.pixel[self.position.x][self.position.y]

        for i in range(ntimes):
            self.screen.pixel[self.position.x][self.position.y] = self.antcolor
            self.screen.update()
            time.sleep(0.01)
            self.screen.pixel[self.position.x][self.position.y] = pixel_color
            self.screen.update()
            time.sleep(0.01)

    def tick(self):
        #self.blink(3)
        self.step()

if __name__ == "__main__":
    from modules.still_image import StillImage
    from screen.virtualscreen import VirtualScreen
    from color_palettes.color_palettes import bw, firenze, colorcombo210
    import pygame

    screen = VirtualScreen()

    rule_length = random.randint(2, 12)
    rule = ""
    for i in range(rule_length):
        rule += random.choice("RL")
    rule = "RL"
    colorlist = random.choice([bw(), firenze(), colorcombo210()])

    print("Langton with rule {} and color: ".format(rule, colorlist))
    still = StillImage(screen, r"C:\Users\Jens\Documents\Code\pixelpi\gallery\pirate.bmp")
    still.start()
    time.sleep(2)
    #still.stop()
    langton = LangtonsAnt(screen, antcolor=Color(255, 0, 0), rule=rule, colorlist=colorlist, clear_screen=False)
    langton.start()

    while True:
        pygame.time.wait(10)
        for event in pygame.event.get():
            pass
