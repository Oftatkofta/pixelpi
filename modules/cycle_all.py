from animation import *
from still_image import *
import time
import os
import random
import input

class CycleAll(Module):
	def __init__(self, screen, interval = 20):
		super(CycleAll, self).__init__(screen)

		input.on_press.append(self.key_press)
		self.paused = False
		
		self.animation_subfolders = self.load_subfolders("animations")
		self.still_filenames = self.load_filenames("gallery")

		self.items = self.animation_subfolders + self.still_filenames
		self.no_display_objects = len(self.items)
		self.display_objects = [None for i in range(self.no_display_objects)]

		self.interval = interval

		self.history = []
		self.history_position = -1
		self.next_animation = time.time()

		self.position = 0

		self.next_animation = time.time()


	def load_filenames(self, location):
		if location[:1] != '/':
			location = location + '/'

		if not os.path.exists(location):
			raise Exception("Path " + location + " not found")

		filenames = [(location+f, "StillImage") for f in listdir(location)]

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

		return subfolders

	def get_current_animation(self):
		if self.history_position < 0:
			return None

		index = self.history[self.history_position]

		if self.display_objects[index] == None:

			if self.items[index][1] == "StillImage":

				self.display_objects[index] = StillImage(self.screen,
				                                        self.items[index][0])

			if self.items[index][1] == "Animation":

				self.display_objects[index] = Animation(self.screen,
				                                        self.items[index][0])

		return self.display_objects[index]
		
	def next(self, pick_random):
		if self.get_current_animation() != None:			
			self.get_current_animation().stop()
		
		
		if self.history_position < len(self.history) - 1:
			self.history_position += 1
			index = self.history[self.history_position]
		else:
			if pick_random:
				index = random.randint(0, len(self.display_objects) - 1)
				self.history_position += 1
			else:
				index = (self.history[self.history_position] + 1) % len(self.display_objects)
				self.history_position += 1
			self.history.append(index)	

		self.get_current_animation().start()
		
	def tick(self):
		if not self.paused and time.time() > self.next_animation:
			self.next(pick_random = True)
			self.next_animation += self.interval
		time.sleep(0.1)

	def on_stop(self):
		if self.get_current_animation() != None:
			self.get_current_animation().stop()

	def key_press(self, key):
		if key == input.Key.RIGHT:
			self.next(pick_random = False)
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
			icon = Animation(self.screen, "icons/pause" if self.paused else "icons/play", interval = 800, autoplay = False)
			icon.play_once()			
			self.get_current_animation().start()
