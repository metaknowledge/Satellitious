import pygame

class Bullet:
  pos: pygame.Vector2
  vel: pygame.Vector2

  def __init__(self, position, velocity) -> None:
    self.pos = position
    self.vel = velocity

  def update(self):
    self.pos += self.vel

  def draw(self, surface):
    pygame.draw.aaline(surface, "green", self.pos, self.pos + self.vel * 10)
