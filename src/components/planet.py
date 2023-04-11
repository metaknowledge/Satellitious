import pygame
from src.components.particle import Particle


import math
from typing import Self
import logging

class Planet(Particle):
  origin: pygame.Vector2
  orbital_radius: float
  frequency: float


  def __init__(self, position: pygame.Vector2, color, objectmass, origin, orbital_radius):
    super().__init__(position, color, objectmass)
    self.origin = origin
    self.orbital_radius = orbital_radius

  def orbit(self, planet: Self):
    #kepler's law of a spherical orbit
    period = math.sqrt(self.orbital_radius / planet.mass)
    self.frequency = 1 / period
    logging.debug(self.frequency)


  def cal_pos(self, time, new_origin):
    if new_origin:
      self.origin = new_origin
    self.pos.x = self.orbital_radius * math.sin(self.frequency * time) + self.origin.x
    self.pos.y = self.orbital_radius * math.cos(self.frequency * time) + self.origin.y

