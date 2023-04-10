import pygame

from src.components.particle import Particle
from src.global_state import GlobalState

class Player(Particle):
  rotation: pygame.Vector2

  def __init__(self, name, position, velocity, color, objectmass, rotation: pygame.Vector2):
    super().__init__(name, position, velocity, color, objectmass)
    self.rotation= rotation

  def update(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        self.vel += self.rotation * 0.01
    if keys[pygame.K_a]:
      self.rotation.rotate_ip(-1)
    if keys[pygame.K_d]:
      self.rotation.rotate_ip(-1)

  def draw_debug(self, screen):
    pygame.draw.aaline(screen, 'green', (self.pos + GlobalState.offset)/GlobalState.zoom, (self.pos + GlobalState.offset + self.rotation*100)/GlobalState.zoom)
    # mouse_position(pygame.mouse.get_pos())
