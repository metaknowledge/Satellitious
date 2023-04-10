import pygame
import math
import random

class Particle:
  name: str
  pos: pygame.Vector2
  vel: pygame.Vector2
  color: str
  mass: float
  radius: float
  static: bool


  def __init__(self, name, position, velocity, color, objectmass):
    self.name = str(name)
    self.pos = position
    self.vel = velocity
    self.color = color
    self.mass = objectmass
    self.radius = math.sqrt(self.mass/math.pi)
    self.static = False
    self.points = []

  @classmethod
  def empty(cls):
    return cls(None, pygame.Vector2(), pygame.Vector2(), None, 0)

  @classmethod
  def random(cls, name, color, lower_mass, upper_mass):
    return cls(name,
              pygame.Vector2(random.randint(-1000, 1000), random.randint(-1000, 1000)),
              pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)),
              color,
              random.uniform(lower_mass, upper_mass)
               )

  def __str__(self) -> str:
    return self.name + str(self.pos)

  def cal_gravity(self, target):
    distance_squared = self.pos.distance_squared_to(target.pos)
    magnitude = target.mass / distance_squared
    acceleration = (target.pos - self.pos).normalize() * min(magnitude, 8)
    return acceleration


  def freeze(self):
    self.static = True

  def draw(self, screen: pygame.surface, offset: pygame.Vector2, zoom: float):
    pygame.draw.circle(screen, self.color, (self.pos + offset)/zoom, max(2, self.radius/zoom), 1)

  def draw_line(self, screen, color, length, multiplyer, windowState):
    relative_position = self.pos + windowState.offset
    pygame.draw.aaline(screen, color, relative_position/windowState.zoom, (relative_position + length*multiplyer)/windowState.zoom)

  def draw_path(self, screen, windowPostion):
    if len(self.points) > 2:
      points = list(map(lambda point: (point + windowPostion.offset)/windowPostion.zoom, self.points))
      pygame.draw.aalines(screen, "yellow", False, points)

  def merge_with(self, target):
    newVel = (self.vel * self.mass + target.vel * target.mass) / (self.mass + target.mass)
    self = Particle(self.name + target.name, self.pos, newVel, self.color, self.mass + target.mass)
