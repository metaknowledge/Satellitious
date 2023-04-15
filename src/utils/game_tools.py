import pygame
from src.components.particle import Particle
from src.components.player import Player
from src.components.planet import Planet


def load_planets() -> list[Planet]:
  # sun = Particle('sun', pygame.Vector2(0,0), pygame.Vector2(0,0), "white", 400)
  # sun = Particle()
  # sun.freeze()
  # earth = Particle('earth' ,pygame.Vector2(0,-500), pygame.Vector2(0.9,0), "green", 20)
  # moon = Particle('moon', pygame.Vector2(0, -234*2), pygame.Vector2(1.6,0), "gray", 0.01)
  # mars = Particle('mars', pygame.Vector2(0, 500*2), pygame.Vector2(-0.7,0), "orange", 20)

  # player = Player('name', pygame.Vector2(1000, 0), pygame.Vector2(0, -0.3), "white", 0.1, pygame.Vector2(0, -1))

  sun = Planet(pygame.Vector2(0,0), "yellow", 100_000, pygame.Vector2(0,0), 0, 1)
  earth = Planet(pygame.Vector2(0,-10000), "green", 500, pygame.Vector2(0,0), 10000, sun.mass)
  # moon = Planet(pygame.Vector2(0, -10100), "red", 2, pygame.Vector2(0, -500), 50, earth.mass)

  jupiter = Planet(pygame.Vector2(0, 0), "orange", 500, pygame.Vector2(0, 0 ), 34000, sun.mass)

  venus = Planet(pygame.Vector2(0, 0), "pink", 150, pygame.Vector2(0, 0), 5500, sun.mass)

  return [sun, earth, jupiter]

def mouse_position(pos):
  pygame.draw.circle(screen, 'white', pos, 1)
  screen.blit(game.fira_code.render(str(pos), true, "white"), pos)
