import pygame
import math

class Particle:
  def __init__(self, name, position, velocity, color, objectmass):
    self.name = name
    self.pos = position
    self.vel = velocity
    self.color = color
    self.mass = objectmass
    self.radius = math.sqrt(self.mass/math.pi)
    self.static = False
    self.points = []

  def cal_gravity(self, target):
    distance_squared = self.pos.distance_squared_to(target.pos)
    magnitude = target.mass / distance_squared
    acceleration = (target.pos - self.pos).normalize() * min(magnitude, 8)
    return acceleration

  def freeze(self):
    self.static = True

  def draw(self):
    pygame.draw.circle(screen, self.color, (self.pos+ global_offset)/global_zoom, max(2, self.radius/global_zoom))

  def draw_line(self, color, length, multiplyer):
    relative_position = self.pos + global_offset
    pygame.draw.aaline(screen, color, relative_position/global_zoom, (relative_position + length*multiplyer)/global_zoom)

  def draw_path(self):
    if len(self.points) > 2:
      points = list(map(lambda point: (point + global_offset)/global_zoom, self.points))
      pygame.draw.aalines(screen, "yellow", False, points)

  def merge_with(self, target):
    newVel = (self.vel * self.mass + target.vel * target.mass) / (self.mass + target.mass)
    newParticle = Particle(self.name + target.name, self.pos, newVel, self.color, self.mass + target.mass)
    if self.static or target.static:
      newParticle.freeze()
    return newParticle