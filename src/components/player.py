import pygame

from src.components.particle import Particle
from src.global_state import GlobalState

class Player(Particle):
  vel: pygame.Vector2
  rotation: pygame.Vector2

  def __init__(self, position,  color, objectmass, velocity: pygame.Vector2, rotation: pygame.Vector2):
    super().__init__(position, color, objectmass)
    self.vel = velocity
    self.rotation = rotation


  def update(self, planets):
    for planet in planets:
      acceleration = self.cal_gravity(planet)
      self.vel += acceleration

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        self.vel += self.rotation * 0.01
    if keys[pygame.K_a]:
      self.rotation.rotate_ip(-1)
    if keys[pygame.K_d]:
      self.rotation.rotate_ip(1)

  def draw_debug(self, screen):
    pygame.draw.aaline(screen, 'green', (self.pos + GlobalState.offset)/GlobalState.zoom, (self.pos + GlobalState.offset + self.rotation*100)/GlobalState.zoom)
    # mouse_position(pygame.mouse.get_pos())
