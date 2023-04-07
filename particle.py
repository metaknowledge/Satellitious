import pygame
import math
from globalVariables import *
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

  def draw(self, windowPostion):
    pygame.draw.circle(screen, self.color, (self.pos+ windowPostion.offset)/windowPostion.zoom, max(2, self.radius/windowPostion.zoom), 1)

  def draw_line(self, color, length, multiplyer, windowPostion):
    relative_position = self.pos + windowPostion.offset
    pygame.draw.aaline(screen, color, relative_position/windowPostion.zoom, (relative_position + length*multiplyer)/windowPostion.zoom)

  def draw_path(self, windowPostion):
    if len(self.points) > 2:
      points = list(map(lambda point: (point + windowPostion.offset)/windowPostion.zoom, self.points))
      pygame.draw.aalines(screen, "yellow", False, points)

  def merge_with(self, target):
    newVel = (self.vel * self.mass + target.vel * target.mass) / (self.mass + target.mass)
    newParticle = Particle(self.name + target.name, self.pos, newVel, self.color, self.mass + target.mass)
    if self.static or target.static:
      newParticle.freeze()
    return newParticle