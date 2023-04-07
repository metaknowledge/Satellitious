import pygame
pygame.init()
screen_size = 4
screen_sizes = pygame.display.list_modes()

screen = pygame.display.set_mode(screen_sizes[screen_size])

class WindowPosition:
  offset = pygame.Vector2(1000,500)
  zoom = 2
  debug = True

windowPostion = WindowPosition()