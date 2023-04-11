import pygame

import pygame
from pygame.locals import *

from src.components.particle import Particle
from src.components.planet import Planet
from src.global_state import GlobalState
from src.services.visualization_service import VisualizationService

import logging

def physics(screen, planets: list[Planet], ticks: int) -> None:
  # for particle in particles:
  #   particle.draw(screen, GlobalState.offset, GlobalState.zoom)
  #   particle.pos += particle.vel
  #   if not particle.static:
  #     for body in particles:
  #       if body is not particle:
  #         acceleration = particle.cal_gravity(body)
  #         particle.vel += acceleration
  #         particle.vel = particle.vel.clamp_magnitude(5)
  #         if GlobalState.debug:
  #           particle.draw_line(screen, 'purple', acceleration, 1000, GlobalState)

  #     if GlobalState.debug:
  #       particle.draw_line(screen, 'red', particle.vel, 30, GlobalState)
  planets[1].cal_pos(ticks / 10000, None)
  planets[2].cal_pos(ticks / 10000, planets[1].pos)
  for planet in planets:
    planet.draw(screen, GlobalState.offset, GlobalState.zoom)


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
def game(screen: pygame.Surface):
  screen.fill("black")
  physics(screen, GlobalState.planets, GlobalState.ticks)
  # collisions(GlobalState.planets)





