import pygame

import pygame
from pygame.locals import *

from src.custom_events import CustomEvents
from src.components.particle import Particle
from src.components.planet import Planet
from src.components.player import Player
from src.global_state import GlobalState
from src.services.visualization_service import VisualizationService
from src.components.game_state import GameState
from src.utils.tools import replace_node
from src.utils.game_tools import load_planets
from src.components.interface_node import InterfaceNode


import logging

def physics(planets: list[Planet], ticks: int, player: Player) -> None:
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
  planets[1].set_new_pos(ticks / 100000, None)
    # planets[].set_new_pos(ticks / 100000, planets[1].pos)
  planets[2].set_new_pos(ticks / 100000, None)
  player.update(planets)
  player.pos += player.vel

def draw_planets(screen, planets: list[Planet], player: Particle):
  for planet in planets:
    planet.draw(screen, GlobalState.offset, GlobalState.zoom)
    planet.draw_orbit(screen, GlobalState.offset, GlobalState.zoom)
  player.draw(screen, GlobalState.offset, GlobalState.zoom)
  player.draw_debug(screen)
  player.draw_line(screen, "green", player.vel * 100, GlobalState.offset, GlobalState.zoom)

def predict_player(planets: list[Planet], player: Particle, ticks: int) -> list[pygame.Vector2]:
  points: list[pygame.Vector2] = [player.pos.copy()]
  vel: pygame.Vector2 = player.vel.copy()
  for i in range(15):
    dt = 1_000_000 * i
    time = (ticks + i*dt) / 100_000
    for planet in planets:
      distance_squared = points[i].distance_squared_to(planet.cal_pos(time))
      magnitude = planet.mass / distance_squared
      acceleration = (planet.cal_pos(time) - points[i]).normalize() * min(magnitude, 8)
      vel += acceleration * (dt/100_000)
    points.append(points[i]+(vel*dt/100_000))
  return points



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
  fira_code = VisualizationService.get_fira_font()
  fps = fira_code.render('fps:' + str(GlobalState.clock.get_fps().__trunc__()), True, "white")
  screen.blit(fps, (0,0))

def main_menu(background: InterfaceNode, menu_buttons: InterfaceNode, settings: InterfaceNode, game_screen: InterfaceNode):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      GlobalState.running = False
    if event.type == pygame.MOUSEBUTTONUP:
      if GlobalState.GAME_STATE == GameState.MAIN_MENU:
        menu_buttons.collide_with_mouse(pygame.Vector2(event.pos))
        settings.collide_with_mouse(pygame.Vector2(event.pos))
    if event.type == CustomEvents.PLAY:
      replace_node(GlobalState.world_ui, background, game_screen)
      GlobalState.GAME_STATE = GameState.GAME
      GlobalState.planets = load_planets()
      logging.debug("changed game!")


#called once every tick
def game(screen: pygame.Surface):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      GlobalState.running = False
    if event.type == pygame.MOUSEWHEEL:
      GlobalState.zoom += event.y * 0.01 * GlobalState.zoom
    if event.type == pygame.KEYDOWN and event.unicode == 'p':
      GlobalState.focus = not GlobalState.focus

  screen.fill("black")
  physics(GlobalState.planets, GlobalState.ticks, GlobalState.player)

  keys = pygame.key.get_pressed()
  if keys[pygame.K_UP]:
    GlobalState.offset.y += GlobalState.zoom * GlobalState.delta * 1000
  if keys[pygame.K_DOWN]:
    GlobalState.offset.y -= GlobalState.zoom * GlobalState.delta * 1000
  if keys[pygame.K_RIGHT]:
    GlobalState.offset.x -= GlobalState.zoom * GlobalState.delta * 1000
  if keys[pygame.K_LEFT]:
    GlobalState.offset.x += GlobalState.zoom * GlobalState.delta * 1000

  if GlobalState.focus:
    target = GlobalState.player.pos.copy()
    new_offset = (pygame.Vector2(screen.get_size()) * GlobalState.zoom / 2) - target
    GlobalState.offset = new_offset

  draw_planets(screen, GlobalState.planets, GlobalState.player)
  draw_fps(screen)
  points = predict_player(GlobalState.planets, GlobalState.player, GlobalState.ticks)
  points = map(GlobalState.true_position, points)
  points = list(points)
  pygame.draw.aalines(screen, "yellow", False, points)
    # collisions(GlobalState.planets)





