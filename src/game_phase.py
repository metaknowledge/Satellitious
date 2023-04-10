import pygame

import pygame
from pygame.locals import *

from src.components.particle import Particle
from src.global_state import GlobalState
from src.services.visualization_service import VisualizationService

import logging

def load_planets() -> list[Particle]:
  sun = Particle('sun', pygame.Vector2(0,0), pygame.Vector2(0,0), "white", 400)
  sun.freeze()
  earth = Particle('earth' ,pygame.Vector2(0,-500), pygame.Vector2(0.9,0), "green", 20)
  moon = Particle('moon', pygame.Vector2(0, -234*2), pygame.Vector2(1.6,0), "gray", 0.01)
  mars = Particle('mars', pygame.Vector2(0, 500*2), pygame.Vector2(-0.7,0), "orange", 20)

  player = Particle('ship', pygame.Vector2(500*2, 0), pygame.Vector2(0,-0.5), "white", 0.01)

  return [sun, earth, mars, moon, player]


def physics(particles: list[Particle]) -> None:
  for particle in particles:
    # particle.draw()
    particle.pos += particle.vel
    if not particle.static:
      for body in particles:
        if body is not particle:
          acceleration = particle.cal_gravity(body)
          particle.vel += acceleration
          particle.vel = particle.vel.clamp_magnitude(5)
          if GlobalState.debug:
            particle.draw_line('purple', acceleration, 1000, GlobalState.SCREEN)

      if GlobalState.debug:
        particle.draw_line('red', particle.vel, 30, GlobalState.SCREEN)


def collisions(planets: list[Particle]) -> None:
  particles = planets.copy()
  while particles:
    particle = particles.pop()
    mergeTargets = []
    for target in particles:
      if particle.pos.distance_to(target.pos) < particle.radius + target.radius:
        mergeTargets.append(target)
    for target in mergeTargets:
      particle.merge_with(target)
      # print(particle, target)
      # particles.remove(particle)
      particles.remove(target)


def track(planets: list[Particle]) -> None:
  for particle in planets:
    if not particle.static:
      particle.points.append(particle.pos.copy())
      if len(particle.points) > 20:
        particle.points.pop(0)

def draw_fps(screen):
  fps = screen.fira_code.render('fps:' + str(GlobalState.clock.get_fps().__trunc__()), True, "white")
  screen.blit(fps, (0,0))

def main_menu():
  logging.info("main menu")

#called once every tick
def game(screen):
  logging.info("game")










