import os.path
import pygame.image
import time
import ConfigParser
from helpers import *
from modules import Module
from PIL import Image

class Animation(Module):
	def __init__(self, screen, folder, interval = None, autoplay = True, fadetime = 1):
		super(Animation, self).__init__(screen)

		if folder[:-1] != '/':
			folder = folder + '/'
		
		self.folder = folder
		self.screen = screen
		self.fadetime = fadetime

		self.config = self.load_config()

		if interval != None:
			self.config["hold"] = int(interval)


		"""
		first try load config, if successful use it

		determine if animation is horizontal or vertical
		single_file AND (height == n*16 OR width == n*16):
			translateX
		"""
		try:
			if self.is_single_file():
				self.load_single()
			else: self.load_frames()
			
			if len(self.frames) == 0:
				raise Exception('No frames found in animation ' + self.folder)
			
			self.screen.pixel = self.frames[0]
		except Exception:
			print('Failed to load ' + folder)
			raise
		
		if self.fadetime != 0:
			self.screen.fade_in(self.fadetime)
		else:
			self.screen.update()
		
		self.pos = 0
		if autoplay:
			self.start()


	def load_frames(self):
		self.frames = []
		i = 0
		while os.path.isfile(self.folder + str(i) + '.bmp'):
			try:

				img = Image.open(self.folder + str(i) + '.bmp')
			except Exception:
				print('Error loading ' + str(i) + '.bmp from ' + self.folder)
				raise


			
			frame = [[rgb_tuple_to_int(img.getpixel((x, y))) for y in range(16)] for x in range(16)]
			self.frames.append(frame)
			
			i += 1
		
	def is_single_file(self):
		return os.path.isfile(self.folder + '0.bmp') and not os.path.isfile(self.folder + '1.bmp')
	
	def load_single(self):
		self.frames = []
		img = Image.open(self.folder + '0.bmp')

		#get framecount from height
		framecount = img.size[1] / 16
			
		for index in range(framecount):
			frame = [[rgb_tuple_to_int(img.getpixel((x, y + 16 * index))) for y in range(16)] for x in range(16)]
			self.frames.append(frame)
	
	def load_interval(self):
		cfg = ConfigParser.ConfigParser()
		cfg.read(self.folder + 'config.ini')
		return cfg.getint('animation', 'hold')

	def load_config(self):
		out = {}
		cfg = ConfigParser.ConfigParser()
		try:
			cfg.read(self.folder + "config.ini")
			out["hold"] = cfg.getint("animation", "hold")
			out["moveX"] = cfg.getint("translate", "moveX")
			out["moveY"] = cfg.getint("translate", "moveY")
			out["loop"] = cfg.getboolean("translate", "loop")
			out["panoff"] = cfg.getboolean("translate", "panoff")
			out["has_config"] = True

		except:
			print('No config found, using defaults')
			out["hold"] = 100
			out["moveX"] = 0
			out["moveY"] = 0
			out["loop"] = True
			out["panoff"] = False
			out["has_config"] = False

		return out


	def tick(self):
		self.pos += 1
		if self.pos >= len(self.frames):
			self.pos = 0
		self.screen.pixel = self.frames[self.pos]
		self.screen.update()
		time.sleep(self.config["hold"] / 1000.0)
		
	def on_start(self):
		print('Starting ' + self.folder)


	def on_stop(self):
		if self.fadetime != 0:
			self.screen.fade_out(self.fadetime)

	def play_once(self):
		for frame in self.frames:
			self.screen.pixel = frame
			self.screen.update()
			time.sleep(self.interval / 1000.0)