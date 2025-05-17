import pygame
from src.components.particle import Particle

import math
import logging

class Planet(Particle):
  origin: pygame.Vector2
  orbital_radius: float
  frequency: float

  def __init__(self, position: pygame.Vector2, color, objectmass, origin, orbital_radius, orbiting_planet_mass):
    super().__init__(position, color, objectmass)
    self.origin = origin
    self.orbital_radius = orbital_radius
    #kepler's law of a spherical orbit
    if self.orbital_radius is not 0:
      self.frequency = (self.orbital_radius / orbiting_planet_mass) ** -0.5
    else:
      self.frequency = 0
    logging.debug(self.frequency)

  def draw_orbit(self, screen, offset, zoom):
    pygame.draw.circle(screen, "gray50", (self.origin + offset)/zoom, self.orbital_radius/zoom, 1)

  def set_new_pos(self, time, new_origin):
    if new_origin:
      self.origin = new_origin
    self.pos.x = self.orbital_radius * math.sin(self.frequency * time) + self.origin.x
    self.pos.y = self.orbital_radius * math.cos(self.frequency * time) + self.origin.y

  def cal_pos(self, time: int) -> pygame.Vector2:
    origin = self.origin
    x = self.orbital_radius * math.sin(self.frequency * time) + origin.x
    y = self.orbital_radius * math.cos(self.frequency * time) + origin.y
    return pygame.Vector2(x,y)