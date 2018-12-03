from screenfactory import create_screen
from modules.snake import Snake
import pygame
import input

screen = create_screen()

snake = Snake(screen)
snake.start()

while True:
	pygame.time.wait(10)
	input.tick()