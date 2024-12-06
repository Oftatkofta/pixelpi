import pygame
import helpers
from screen import AbstractScreen

# Behaves like the actual LED screen, but shows the screen content on a computer screen
class VirtualScreen(AbstractScreen):
	def __init__(self, width = 16, height = 16, led_pin = 18, led_freq_hz = 800000, led_dma = 5, led_invert = False, led_brightness = 200):		
		super(VirtualScreen, self).__init__(width, height)
		self.pixel_size = 30
		
		pygame.display.init()
		self.screen = pygame.display.set_mode((width * self.pixel_size,
												height * self.pixel_size),
												pygame.RESIZABLE)

		self.surface = pygame.Surface(self.screen.get_size())	

def update(self):
    """
    Updates the virtual screen by drawing the LED matrix to the Pygame surface and displaying it.
    This method converts the internal GRB color format to RGB for proper display.
    """
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            # Update the screen size
            self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            self.surface = pygame.Surface(self.screen.get_size())
    
    for y in range(self.height):
        for x in range(self.width):
            # Convert GRB color format to RGB for display
            adjusted_color = helpers.int_to_rgb_color(self.pixel[x][y])
            pygame.draw.rect(self.surface, adjusted_color, ((x * self.pixel_size, y * self.pixel_size), (((x+1) * self.pixel_size), (y+1) * self.pixel_size)))

    self.screen.blit(self.surface, (0, 0))
    pygame.display.flip()  # flip() is enough since we're updating the whole screen