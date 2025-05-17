import pygame
from src.services.visualization_service import VisualizationService
import random
import logging

class Asteroid(pygame.sprite.Sprite):
  pos: pygame.Vector2
  vel: pygame.Vector2
  image: pygame.Surface
  rect: pygame.Rect
  mask: pygame.Mask

  def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, level: int) -> None:
    pygame.sprite.Sprite.__init__(self)
    if bool(random.getrandbits(1)):
      self.image = VisualizationService.get_asteroid_img_one()
    else:
      self.image = VisualizationService.get_asteroid_img_two()
    self.image = pygame.transform.scale_by(self.image, level/10)
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.pos = position
    self.vel = velocity

  @classmethod
  def random(cls, position: pygame.Vector2, level: int):
    velocity = pygame.Vector2(random.uniform(-1,1)/level, random.uniform(-1,1)/level)
    return cls(position, velocity, level)

  def update(self, surface: pygame.Surface, acceleration) -> None:
    self.vel -= acceleration
    self.pos += self.vel
    surface.blit(self.image, self.rect.center + self.pos)
    logging.info(self.vel)
