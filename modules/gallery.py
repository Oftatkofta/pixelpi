
from animation import Animation
import time
from os import listdir
from helpers import Color, rgb_tuple_to_int
from PIL import Image
import input
from random import shuffle

class Gallery(Module):
	def __init__(self, screen):
		super(Gallery, self).__init__(screen)

		input.on_press.append(self.key_press)
		self.paused = False
		
		self.filenames = self.load_filenames("gallery")

		self.images = [None for i in range(len(self.filenames))]
		
		self.interval = 10
		self.position = 0

		self.next_animation = time.time()

	def load_filenames(self, location):
		if location[:1] != '/':
			location = location + '/'
		
		if not os.path.exists(location):
			raise Exception("Path " + location + " not found")
		
		filenames = [location + f for f in listdir(location)]

		#randomize order of files each time
		shuffle(filenames)
		
		if len(filenames) == 0:
			raise Exception("No images found in " + location)

		return filenames

	def move(self, amount):
		self.position = (self.position + amount) % len(self.filenames)
		self.screen.fade_out(1)
		if self.images[self.position] == None:
			self.load(self.position)
			print("loading: ", self.filenames[self.position])
		self.draw()

	def load(self, index):
		try:
			image = Image.open(self.filenames[index])
		except Exception:
			print('Error loading ' + self.filenames[index])
			raise


		if image.size != (16,16):
			print("resizing:", self.filenames[index])
			image = image.resize((16,16), resample=Image.LANCZOS)
		if image.mode != "RGB":
			# avoid alpha channel for now
			print("converting:", self.filenames[index], image.mode)
			image = image.convert("RGB")



		self.images[index] = [[rgb_tuple_to_int(image.getpixel((x, y))) for y in range(16)] for x in range(16)]

	def draw(self):
		self.screen.pixel = self.images[self.position]
		self.screen.fade_in(1)
		#self.screen.update()

	def tick(self):
		if not self.paused and time.time() > self.next_animation:
			self.move(1)
			self.next_animation += self.interval
		time.sleep(0.1)

	def key_press(self, key):
		if key == input.Key.RIGHT:
			self.move(1)
			self.next_animation = time.time() + self.interval
		if key == input.Key.LEFT:
			self.move(-1)
			self.next_animation = time.time() + self.interval
		if key == input.Key.A or key == input.Key.ENTER:
			self.paused = not self.paused
			if not self.paused:
				self.next_animation = time.time() + self.interval
			icon = Animation(self.screen, "icons/pause" if self.paused else "icons/play", interval = 800, autoplay = False)
			icon.play_once()			
			self.draw()