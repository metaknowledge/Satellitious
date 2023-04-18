import pygame
from src.components.particle import Particle
from src.components.player import Player
from src.components.planet import Planet


def load_planets() -> list[Planet]:
  origin = pygame.Vector2(0,0)
  sun = Planet(pygame.Vector2(0,0), "yellow", 300_000, origin, 0, 1)
  earth = Planet(pygame.Vector2(0,0), "chartreuse4", 500, origin, 10000, sun.mass)

  jupiter = Planet(pygame.Vector2(0, 0), "coral1", 500, origin, 34000, sun.mass)

  neptune = Planet(pygame.Vector2(0,0), "light blue", 1000, origin, 50000, sun.mass)

  # moon = Planet(pygame.Vector2(0, -10100), "red", 2, pygame.Vector2(0, -500), 50, earth.mass)
  #venus = Planet(pygame.Vector2(0, -5500), "pink", 150, origin, 5500, sun.mass)

  return [sun, earth, jupiter, neptune]

def mouse_position(pos):
  pygame.draw.circle(screen, 'white', pos, 1)
  screen.blit(game.fira_code.render(str(pos), true, "white"), pos)
