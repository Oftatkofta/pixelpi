import time
import os
import random

from modules import Module
from modules.clock2 import Clock2
from modules.text_scroller import TextScroller
from modules.fire import Fire
from modules.langtons_ant import LangtonsAnt
from modules.pie import Pie
from modules.animation import Animation
from modules.still_image import StillImage
from helpers import Color, Point
from color_palettes.color_palettes import bw, firenze, colorcombo210


class CycleAllXmas(Module):
    """
    Randomly picks a module to run from the a list. If the module is a StillImage or Animation
    then a random file/folder will be displayed. It will display the clock at a set interval.

    interval: Time in seconds to display Module
    fadetime: Time of transition fade in seconds
    """

    def __init__(self, screen, interval=20, fadetime=0.1):
        super(CycleAllXmas, self).__init__(screen)

        self.interval = interval
        self.fadetime = fadetime
        self.modules_to_load = ["Text1", "Text2", "Fire", "Langton", "Pie", "StillImage", "Animation"]

        #Preloads the persistent modules that remember their states
        self.clock = Clock2(self.screen, fadetime=self.fadetime)
        self.text1 = TextScroller(self.screen, "THIS IS TEXT 1!", color=Color(255, 255, 255), speed=0.2)
        self.text2 = TextScroller(self.screen, "GITHUB: Oftatkofta/pixelpi", color=Color(255, 0, 0), speed=0.1, y_position=9)
        self.fire = Fire(self.screen)
        self.pie = Pie(self.screen)

        self.animation_subfolders = self.load_subfolders("animations")
        self.still_filenames = self.load_filenames("gallery")

        self.when_to_pick_next_module = time.time()
        self.total_displays = 0

        self.pick_clock_flag = False
        self.module_to_load = self.pick_module()

        #Holds the currently loaded module
        self.current_module = self.load_module(self.module_to_load)

    def load_filenames(self, location):
        if location[:1] != '/':
            location = location + '/'

        if not os.path.exists(location):
            raise Exception("Path " + location + " not found")

        filenames = [location + f for f in os.listdir(location)]


        if len(filenames) == 0:
            raise Exception("No images found in " + location)

        return filenames

    def load_subfolders(self, location):
        if location[:1] != '/':
            location = location + '/'

        if not os.path.exists(location):
            raise Exception("Path " + location + " not found")

        subfolders = [x[0] for x in os.walk(location)]

        #discard first value which is the root folder
        subfolders = subfolders[1:]

        if len(subfolders) == 0:
            raise Exception("No subfolders found in " + location)

        return subfolders

    def pick_module(self):
        """
        if the pick_clock_flag is not set, then it returns the name of a random module.

        :return:
            (str) Name of Module to load
        """
        if not self.pick_clock_flag:
            return random.choice(self.modules_to_load)

        else:
            return "Clock"

    def load_module(self, modulename):

        if modulename == "Clock":
            return self.clock

        if modulename == "Text1":
            return self.text1

        if modulename == "Text2":
            self.when_to_pick_next_module -= self.interval / 2.0
            return self.text2

        if modulename == "Fire":
            return self.fire

        if modulename == "Langton":
            rule_length = random.randint(2,12)
            rule = ""
            for i in range(rule_length):
                rule += random.choice("RL")

            colorlist = random.choice([bw(), firenze(), colorcombo210()])

            print("Langton with rule {} and color: ".format(rule, colorlist))

            return LangtonsAnt(self.screen, antcolor=Color(255, 0, 0), rule=rule, colorlist=colorlist)

        if modulename == "Pie":
            return self.pie

        if modulename == "StillImage":

            return StillImage(self.screen, filename=random.choice(self.still_filenames), fadetime=self.fadetime)

        if modulename == "Animation":

            return Animation(self.screen, random.choice(self.animation_subfolders), fadetime=self.fadetime)


    def get_current_module(self):

            return self.current_module


    def next(self):

        self.get_current_module().stop()

        self.module_to_load = self.pick_module()
        self.current_module = self.load_module(self.module_to_load)

        self.get_current_module().start()

    def tick(self):
        if time.time() > self.when_to_pick_next_module:

            self.next()

            if self.pick_clock_flag:
                self.when_to_pick_next_module += self.interval / 2.0

            else:
                self.when_to_pick_next_module += self.interval

            self.pick_clock_flag = not self.pick_clock_flag
            self.total_displays += 1

            print("Tick, total displays: {}, pick clock: {}".format(self.total_displays, self.pick_clock_flag))

        time.sleep(0.01)

    def on_stop(self):
        if self.get_current_module() != None:
            self.get_current_module().stop()
