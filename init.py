import pygame
import os

pygame.init()

# screen
screen_size = 2
screen_sizes = pygame.display.list_modes()
screen = pygame.display.set_mode(screen_sizes[screen_size])

# clock
clock = pygame.time.Clock()

# other variables
offset = pygame.Vector2(1000,500)
zoom = 2
debug = True