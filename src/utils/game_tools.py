import pygame
from src.components.particle import Particle
from src.components.player import Player

def load_planets() -> list[Particle]:
  sun = Particle('sun', pygame.Vector2(0,0), pygame.Vector2(0,0), "white", 400)
  sun.freeze()
  earth = Particle('earth' ,pygame.Vector2(0,-500), pygame.Vector2(0.9,0), "green", 20)
  moon = Particle('moon', pygame.Vector2(0, -234*2), pygame.Vector2(1.6,0), "gray", 0.01)
  mars = Particle('mars', pygame.Vector2(0, 500*2), pygame.Vector2(-0.7,0), "orange", 20)

  player = Player('name', pygame.Vector2(1000, 0), pygame.Vector2(0, -0.3), "white", 0.1, pygame.Vector2(0, -1))

  return [player, sun, earth, mars, moon]
