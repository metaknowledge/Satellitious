# Example file showing a basic pygame "game loop"
import pygame
from pygame.locals import *
import os
import math
from particle import Particle
from globalVariables import *

pygame.display.set_icon(pygame.image.load(os.path.join("imgs", "ikon.png")))

pygame.display.set_caption('gravity game')
pygame.display.set_mode(screen_sizes[screen_size])
print(pygame.display.list_modes())

clock = pygame.time.Clock()
running = True
speed = 1


def physics():
  for object in objects:
    object.draw(windowPostion)
    object.pos += object.vel
    if not object.static:
      for body in objects:
        if body is not object:
          acceleration = object.cal_gravity(body)
          object.vel += acceleration
          object.vel = object.vel.clamp_magnitude(15)
          if windowPostion.debug:
            object.draw_line('purple', acceleration, 1000, windowPostion)

    if windowPostion.debug:
      object.draw_line('red', object.vel, 30, windowPostion)
      object.draw_path(windowPostion)

def collisions():
  particles = objects.copy()
  while particles:
    particle = particles.pop()
    mergeTargets = []
    for target in particles:
      if particle.pos.distance_to(target.pos) < particle.radius + target.radius:
        mergeTargets.append(target)
    for target in mergeTargets:
      objects.append(particle.merge_with(target))
      objects.remove(target)
      objects.remove(particle)

def tracking():
  for particle in objects:
    if not particle.static:
      particle.points.append(particle.pos.copy())
      if len(particle.points) > 10:
        particle.points.pop(0)

def post_quit():
  pygame.event.post(pygame.event.Event(QUIT))

def toggle_debug(key):
  windowPostion.debug = not windowPostion.debug

sun = Particle('sun', pygame.Vector2(0,0), pygame.Vector2(0,0), "white", 400)
sun.freeze()
earth = Particle('earth' ,pygame.Vector2(0,-500), pygame.Vector2(1,0), "green", 20)
moon = Particle('moon', pygame.Vector2(0, -234*2), pygame.Vector2(1.8,0), "gray", 0.01)
mars = Particle('mars', pygame.Vector2(0, 500*2), pygame.Vector2(-0.7,0), "orange", 20)

player = Particle('ship', pygame.Vector2(500*2, 0), pygame.Vector2(0,-0.5), "white", 0.01)
playerRotation = pygame.Vector2(0,-1)
objects = [sun, earth, mars, moon, player]

key_subs = {'f': [pygame.display.toggle_fullscreen],
            'q': [post_quit],
            '': {
              '1073741884': [toggle_debug],
              },
            'w': [],
            'a':[],
            's':[],
            'd':[]
            }

ONE_SECOND_TIMER = pygame.event.custom_type()
pygame.time.set_timer(ONE_SECOND_TIMER, 1000)

while running:

  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == MOUSEWHEEL:
      windowPostion.zoom += event.y * 0.01 * windowPostion.zoom
      print(windowPostion.zoom)
      # if event.y != 0:
      #   window_area = pygame.Vector2(pygame.display.get_window_size())
      #   bottom_right = windowPostion.offset + window_area/windowPostion.zoom
      #   midpoint = bottom_right/2
      #   windowPostion.offset += (midpoint - (midpoint - windowPostion.offset) / (1 - (event.y *0.1)))
      #   print(midpoint, windowPostion.offset, windowPostion.zoom, event.y* 0.1)
    elif event.type == KEYDOWN:
      print(event)
      if event.unicode == '' and str(event.key) in key_subs[event.unicode]:
        for func in key_subs[event.unicode][str(event.key)]:
          func(event.key)
      elif event.unicode != '' and event.unicode in key_subs:
        for func in key_subs[event.unicode]:
          func()
    elif event.type == ONE_SECOND_TIMER:
      tracking()

  # fill the screen with a color to wipe away anything from last frame
  screen.fill("black")

  keys = pygame.key.get_pressed()
  if keys[pygame.K_w]:
      player.vel += playerRotation * 0.01
  if keys[pygame.K_a]:
    playerRotation.rotate_ip(-1)
  if keys[pygame.K_d]:
    playerRotation.rotate_ip(1)
  if keys[pygame.K_UP]:
    windowPostion.offset.y += speed * windowPostion.zoom
  if keys[pygame.K_DOWN]:
    windowPostion.offset.y -= speed * windowPostion.zoom
  if keys[pygame.K_RIGHT]:
    windowPostion.offset.x -= speed * windowPostion.zoom
  if keys[pygame.K_LEFT]:
    windowPostion.offset.x += speed * windowPostion.zoom
  # print(player_rotation)
  if player and windowPostion.debug:
    pygame.draw.aaline(screen, 'green', (player.pos + windowPostion.offset)/windowPostion.zoom, (player.pos + windowPostion.offset + playerRotation*100)/windowPostion.zoom)

  collisions()
  physics()


  pygame.display.flip()
  clock.get_fps()
  clock.tick(60)  # limits FPS to 60
pygame.quit()
