import pygame
import math
import random
from typing import Self

class Particle:
  pos: pygame.Vector2
  color: str
  mass: float
  particle_radius: float

  def __init__(self, position,  color, objectmass):
    self.pos = position
    self.color = color
    self.mass = objectmass
    self.particle_radius = math.sqrt(self.mass/math.pi)

  def cal_gravity(self, target: Self):
    distance_squared = self.pos.distance_squared_to(target.pos)
    magnitude = target.mass / distance_squared
    acceleration = (target.pos - self.pos).normalize() * min(magnitude, 8)
    return acceleration

  def draw(self, screen: pygame.surface, offset: pygame.Vector2, zoom: float):
    pygame.draw.circle(screen, self.color, (self.pos + offset)/zoom, max(2, self.particle_radius/zoom))

  def draw_line(self, screen, color, length, offset: pygame.Vector2, zoom: pygame.Vector2):
    relative_position = self.pos + offset
    pygame.draw.aaline(screen, color, relative_position/zoom, (relative_position + length)/zoom)

  def merge_with(self, target):
    self = Particle(self.pos, self.color, self.mass + target.mass)
