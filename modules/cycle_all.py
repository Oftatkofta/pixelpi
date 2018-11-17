from animation import *
from clock2 import *
from still_image import *
import time
import os
import random
import input


class CycleAll(Module):
	"""
	Loads all filenames and animation folders, Creates lists of different module
	 objects and displays them randomly. It will display the clock at a regular
	 set interval.

	Remembers a history of 50-100 in case you want to go back or forward with
	an imput device

	"""

	def __init__(self, screen, interval=20, fadetime=0):
		super(CycleAll, self).__init__(screen)

		input.on_press.append(self.key_press)
		self.paused = False

		self.animation_subfolders = self.load_subfolders("animations")
		self.still_filenames = self.load_filenames("gallery")

		self.items_to_load =["clock"] + self.animation_subfolders + self.still_filenames
		self.no_display_objects = len(self.items_to_load)
		self.display_objects = [None for i in range(self.no_display_objects)]

		self.clock = Clock2(self.screen)
		self.pick_clock = False


		# The first display_objects are special modules that are displayed
		# more frequently
		self.display_objects[0] = self.clock

		self.interval = interval
		self.fadetime = fadetime

		self.index_history = []
		self.history_position = -1
		self.next_animation = time.time()

		self.total_displays = 0

		self.next_animation = time.time()

	def load_filenames(self, location):
		if location[:1] != '/':
			location = location + '/'

		if not os.path.exists(location):
			raise Exception("Path " + location + " not found")

		filenames = [(location + f, "StillImage") for f in listdir(location)]

		# randomize order of files each time
		shuffle(filenames)

		if len(filenames) == 0:
			raise Exception("No images found in " + location)

		return filenames

	def load_subfolders(self, location):
		if location[:1] != '/':
			location = location + '/'

		if not os.path.exists(location):
			raise Exception("Path " + location + " not found")
		subfolders = [(x[0], "Animation") for x in os.walk(location)]

		subfolders = subfolders[1:]

		if len(subfolders) == 0:
			raise Exception("No animations found in " + location)

		shuffle(subfolders)

		return subfolders

	def get_current_animation(self):
		if self.history_position < 0:
			return None

		index = self.index_history[self.history_position]

		if self.display_objects[index] == None:

			if self.items_to_load[index][1] == "StillImage":
				self.display_objects[index] = StillImage(self.screen,
				                                         self.items_to_load[
					                                         index][0],
				                                         fadetime=self.fadetime)

			if self.items_to_load[index][1] == "Animation":
				self.display_objects[index] = Animation(self.screen,
				                                        self.items_to_load[
					                                        index][0],
				                                        autoplay=False,
				                                        fadetime=self.fadetime)

		return self.display_objects[index]

	def next(self, pick_clock=False, pick_random=True):

		if self.get_current_animation() != None:
			self.get_current_animation().stop()

		if len(self.index_history) > 100:
			# Don't save an infinite history, 50-100 items seems reasonable
			del self.index_history[:50]
			self.history_position -= 50

		if pick_random and not pick_clock:
			index = random.randint(1, len(self.display_objects) - 1)

		elif pick_clock:
			index = 0
		else:
			if self.history_position == -1:
				index = 0
			else:
				index = (self.index_history[self.history_position] + 1) % len(
					self.display_objects)

		self.history_position += 1
		self.index_history.append(index)

		self.get_current_animation().start()

	def tick(self):
		if not self.paused and time.time() > self.next_animation:
			self.next(pick_clock=self.pick_clock)

			if self.pick_clock:
				self.next_animation += self.interval/2.0

			else:
				self.next_animation += self.interval

			self.pick_clock = not self.pick_clock
			self.total_displays += 1

			print(self.total_displays)

		time.sleep(0.1)

	def on_stop(self):
		if self.get_current_animation() != None:
			self.get_current_animation().stop()

	def key_press(self, key):
		if key == input.Key.RIGHT:
			self.next(pick_random=False)
		if key == input.Key.LEFT:
			if self.history_position > 0:
				self.get_current_animation().stop()
				self.history_position -= 1
				self.get_current_animation().start()
		if key == input.Key.A or key == input.Key.ENTER:
			self.paused = not self.paused
			if not self.paused:
				self.next_animation = time.time() + self.interval
			self.get_current_animation().stop()
			icon = Animation(self.screen,
			                 "icons/pause" if self.paused else "icons/play",
			                 interval=800, autoplay=False)
			icon.play_once()
			self.get_current_animation().start()
