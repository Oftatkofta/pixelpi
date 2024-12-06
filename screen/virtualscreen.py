import pygame
import helpers
from screen import AbstractScreen

class VirtualScreen(AbstractScreen):
	"""
	VirtualScreen simulates an LED screen using Pygame to render the display on a computer screen.
	
	Attributes:
		pixel_size (int): Size of each 'pixel' on the virtual screen.
		screen (pygame.Surface): The Pygame window surface where the virtual screen is displayed.
		surface (pygame.Surface): The Pygame surface that is used to draw the virtual screen content.
	"""
	def __init__(self, width=16, height=16, led_pin=18, led_freq_hz=800000, led_dma=5, led_invert=False, led_brightness=200):
		"""
		Initializes a new VirtualScreen instance with the given dimensions and LED parameters.
		
		Args:
			width (int): The width of the virtual screen in pixels. Defaults to 16.
			height (int): The height of the virtual screen in pixels. Defaults to 16.
			led_pin (int): The GPIO pin connected to the LED strip. Defaults to 18.
			led_freq_hz (int): The frequency of the LED signal in hertz. Defaults to 800000.
			led_dma (int): The DMA channel used for generating the PWM signal. Defaults to 5.
			led_invert (bool): Whether to invert the LED signal. Defaults to False.
			led_brightness (int): The brightness of the LEDs. Defaults to 200.
		"""
		super(VirtualScreen, self).__init__(width, height)
		self.pixel_size = 30
		
		pygame.display.init()
		self.screen = pygame.display.set_mode((width * self.pixel_size,
												height * self.pixel_size),
												pygame.RESIZABLE)

		self.surface = pygame.Surface(self.screen.get_size())    

	def update(self):
		for y in range(self.height):
			for x in range(self.width):
				#colors are in GRB format on the LED strip, to display properly we need to convert to a RGB tuple
				adjusted_color = helpers.int_to_rgb_color(self.pixel[x][y])
				pygame.draw.rect(self.surface, adjusted_color, ((x * self.pixel_size, y * self.pixel_size), (((x+1) * self.pixel_size), (y+1) * self.pixel_size)))
				self.screen.blit(self.surface, (0, 0))
		pygame.display.flip()
		pygame.display.update()