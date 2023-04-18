import pygame

import pygame
from pygame.locals import *

from src.custom_events import CustomEvents
from src.components.particle import Particle
from src.components.planet import Planet
from src.components.player import Player
from src.global_state import GlobalState
from src.services.visualization_service import VisualizationService
from src.components.game_state import GameState, AsteroidBelt
from src.utils.tools import replace_node, add_tuples
from src.utils.game_tools import load_planets
from src.components.interface_node import InterfaceNode, Button
from src.components.asteroid import Asteroid

import logging
import random


def physics(planets: list[Planet], ticks: int, player: Player) -> None:
  for planet in planets:
    planet.set_new_pos(ticks / 100000, None)
  player.update(planets)
  player.pos += player.vel
  distance = player.pos.distance_to(pygame.Vector2(0,0))
  if distance > 21000 and distance < 23000:
    GlobalState.asteroid_belt = AsteroidBelt.EASY
  elif distance > 39000 and distance < 41000:
    GlobalState.asteroid_belt = AsteroidBelt.MEDIUM
  elif distance > 55000 and distance < 57000:
    GlobalState.asteroid_belt = AsteroidBelt.HARD
  else:
    GlobalState.asteroid_belt = None

def draw_planets(screen, planets: list[Planet], player: Player):
  for planet in planets:
    planet.draw(screen, GlobalState.offset, GlobalState.zoom)
    planet.draw_orbit(screen, GlobalState.offset, GlobalState.zoom)
  player.draw(screen, GlobalState.offset, GlobalState.zoom)
  player.draw_debug(screen)
  player.draw_line(screen, "green", player.vel * 100, GlobalState.offset, GlobalState.zoom)

def draw_asteroid_belts(screen: pygame.Surface):
  #easy
  pygame.draw.circle(screen, "green", GlobalState.true_position(pygame.Vector2(0,0)), 21000/GlobalState.zoom, 1)
  pygame.draw.circle(screen, "green", GlobalState.true_position(pygame.Vector2(0,0)), 23000/GlobalState.zoom, 1)
  #medium
  pygame.draw.circle(screen, "orange", GlobalState.true_position(pygame.Vector2(0,0)), 39000/GlobalState.zoom, 1)
  pygame.draw.circle(screen, "orange", GlobalState.true_position(pygame.Vector2(0,0)), 41000/GlobalState.zoom, 1)
  #hard
  pygame.draw.circle(screen, "red", GlobalState.true_position(pygame.Vector2(0,0)), 55000/GlobalState.zoom, 1)
  pygame.draw.circle(screen, "red", GlobalState.true_position(pygame.Vector2(0,0)), 57000/GlobalState.zoom, 1)

def draw_asteroid_belt_level(screen: pygame.Surface):
  if GlobalState.asteroid_belt:
    level = VisualizationService.get_boxy_font(40).render(f"asteroid belt level: {GlobalState.asteroid_belt.name}",True, AsteroidBelt.get_color(GlobalState.asteroid_belt), "black")
    screen.blit(level, (0, screen.get_height() - level.get_height()))
  else:
    level = VisualizationService.get_boxy_font(40).render("Move into asteroid belt", True, "white", "black")
    screen.blit(level, (0, screen.get_height() - level.get_height()))


def predict_player(planets: list[Planet], player: Particle, ticks: int) -> list[pygame.Vector2]:
  points: list[pygame.Vector2] = [player.pos.copy()]
  vel: pygame.Vector2 = player.vel.copy()
  dt = 1_000_000
  for i in range(30):
    time = (ticks + i*dt) / 100_000
    for planet in planets:
      distance_squared = points[i].distance_squared_to(planet.cal_pos(time))
      magnitude = planet.mass / distance_squared
      acceleration = (planet.cal_pos(time) - points[i]).normalize() * min(magnitude, 8)
      dt = 1_000_000 * i -  1_000 * magnitude
      vel += acceleration * (dt/100_000)
    points.append(points[i]+(vel*dt/100_000))
  return points

def draw_space_ship(screen: pygame.Surface):
  rotation = GlobalState.player.rotation.angle_to(pygame.Vector2(0, -1))
  screen_middle = pygame.Vector2(screen.get_size()) / 2
  player_front = pygame.Vector2(0, -30).rotate(-rotation)
  player_left_tail= pygame.Vector2(-15, 10).rotate(-rotation)
  player_right_tail = pygame.Vector2(15, 10).rotate(-rotation)
  player_back_left = pygame.Vector2(-11.25, 0).rotate(-rotation)
  player_back_right = pygame.Vector2(11.25, 0).rotate(-rotation)
  player_back_thrust = pygame.Vector2(0, 15).rotate(-rotation)
  pygame.draw.aaline(screen, 'white', player_front + screen_middle, player_left_tail + screen_middle)
  pygame.draw.aaline(screen, 'white', player_front + screen_middle, player_right_tail + screen_middle)
  pygame.draw.aaline(screen, 'white', player_back_left + screen_middle, player_back_right + screen_middle)
  if GlobalState.accelerating:
    pygame.draw.aaline(screen, 'white', player_back_left + screen_middle, player_back_thrust + screen_middle)
    pygame.draw.aaline(screen, 'white', player_back_right + screen_middle, player_back_thrust + screen_middle)


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

def draw_fps(screen):
  fps = VisualizationService.get_boxy_font(40).render('fps:' + str(GlobalState.clock.get_fps().__trunc__()), True, "white")
  screen.blit(fps, (0,0))

def main_menu():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      GlobalState.running = False
    if event.type == pygame.MOUSEBUTTONUP:
      mouse_position = pygame.Vector2(event.pos)
      for button in GlobalState.menu_buttons.sprites():
        button.collide_with_mouse(mouse_position)
    if event.type == CustomEvents.SETTINGS:
      replace_node(GlobalState.world_ui, GlobalState.main_menu_screen, GlobalState.settings_screen)
      GlobalState.GAME_STATE = GameState.SETTINGS
      logging.info("settings")

    if event.type == CustomEvents.PLAY:
      replace_node(GlobalState.world_ui, GlobalState.main_menu_screen, GlobalState.game_screen)
      GlobalState.GAME_STATE = GameState.GAME
      GlobalState.planets = load_planets()
      logging.info("changed game!")

def settings():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      GlobalState.running = False
    if event.type == pygame.MOUSEBUTTONUP:
      mouse_position = pygame.Vector2(event.pos)
      # for child in close_button.children.sprites():
      for button in GlobalState.settings_buttons.sprites():
        button.collide_with_mouse(mouse_position)
        logging.info(button.rect)
    if event.type == CustomEvents.MENU:
      logging.info("menu")
      replace_node(GlobalState.world_ui, GlobalState.settings_screen, GlobalState.main_menu_screen)
      # GlobalState.load_user_interface()
      GlobalState.GAME_STATE = GameState.MAIN_MENU

def summon_asteroids():

  if len(GlobalState.asteroid_group.sprites()) <= 10:
    GlobalState.asteroid_group.add(Asteroid.random())


#called once every tick
def game():
  screen = GlobalState.game_screen.image
  screen.fill('black')
  GlobalState.accelerating = False
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      GlobalState.running = False
    if event.type == pygame.MOUSEWHEEL and GlobalState.hidden_map:
      GlobalState.zoom += event.y * 0.01 * GlobalState.zoom
    if event.type == pygame.KEYDOWN:
      if event.unicode == 'p':
        GlobalState.focus = not GlobalState.focus
      elif event.unicode == 'm':
        GlobalState.hidden_map = not GlobalState.hidden_map

  physics(GlobalState.planets, GlobalState.ticks, GlobalState.player)

  keys = pygame.key.get_pressed()
  draw_space_ship(screen)

  space_map = GlobalState.space_map
  space_map.fill("black")
  # for asteroid in GlobalState.asteroid_belt:
  #   if asteroid.pos

  if GlobalState.asteroid_belt:
     if len(GlobalState.asteroid_group.sprites()) <= 10:
      x = random.randint(-1000, 1100)
      y = random.randint(-1000, 1100)

      GlobalState.asteroid_group.add(Asteroid.random(pygame.Vector2(x,y), 1))

  if GlobalState.hidden_map:
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
      new_offset = (pygame.Vector2(space_map.get_size()) * GlobalState.zoom / 2) - target
      GlobalState.offset = new_offset
    draw_asteroid_belts(space_map)
    draw_planets(space_map, GlobalState.planets, GlobalState.player)
    draw_fps(space_map)
    draw_asteroid_belt_level(space_map)
    points = predict_player(GlobalState.planets, GlobalState.player, GlobalState.ticks)
    points = map(GlobalState.true_position, points)
    points = list(points)
    pygame.draw.aalines(space_map, "yellow", False, points)
    screen.blit(space_map, (0, 0))
  GlobalState.asteroid_group.update(screen)






