import time
from helpers import *
from modules import Module
from itertools import cycle, islice
from color_palettes import color_palettes
import os


class LangtonsAnt(Module):
    """
    Implemets Langton's ant on a toroidal grid (top-bottom, left-righ wrapping)

    The rules are:
    On white turn right, on black turn left, flip the color of the square
    """

    def __init__(self, screen, start_position=Point(randint(0, 15), randint(0, 15)),
                 antcolor=Color(255, 0, 0), rule="RLLRL", colorlist=color_palettes.firenze(),
                 clear_screen=True):
        super(LangtonsAnt, self).__init__(screen)

        self.position = start_position
        self.previous_position = None
        self.antcolor = antcolor

        self.rule = list(rule)
        self.colors = colorlist[:len(self.rule)]
        self.color_cycle = cycle(self.colors)
        next(self.color_cycle)

        self.rulebook = dict(list(zip(self.colors,
                                 list(zip(self.rule, self.color_cycle)))))

        if clear_screen:
            self.screen.clear_pixel(next(self.color_cycle))

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
# self.blink()
