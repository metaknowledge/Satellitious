# Example file showing a basic pygame "game loop"
import pygame
from pygame.locals import *
import os
import math

# pygame setup
pygame.init()
screen_size = 2
screen_sizes = pygame.display.list_modes()

pygame.display.set_icon(pygame.image.load(os.path.join("imgs", "ikon.png")))

screen = pygame.display.set_mode(screen_sizes[2])

pygame.display.set_caption('gravity game')

print(pygame.display.list_modes())

clock = pygame.time.Clock()
running = True
debug = True
WHITE = (255,255,255)
BLACK = (0,0,0)

global_offset = pygame.Vector2(1000,500)
global_zoom = 2
speed = 1


class Particle:
  def __init__(self, name, position, velocity, color, objectmass):
    self.name = name
    self.pos = position
    self.vel = velocity
    self.color = color
    self.mass = objectmass
    self.static = False
    self.points = []

  def cal_gravity(self, target):

    magnitude = target.mass / self.pos.distance_squared_to(target.pos)

    acceleration = (target.pos - self.pos).normalize() * magnitude

    return acceleration

  def freeze(self):
    self.static = True

  def draw(self):
    pygame.draw.circle(screen, self.color, (self.pos+ global_offset)/global_zoom, max(2, math.log(self.mass)*2))

  def draw_line(self, color, length, multiplyer):
    relative_position = self.pos + global_offset
    pygame.draw.aaline(screen, color, relative_position/global_zoom, (relative_position + length*multiplyer)/global_zoom)

  def draw_path(self):
    if len(self.points) > 2:
      points = list(map(lambda point: (point + global_offset)/global_zoom, self.points))
      pygame.draw.aalines(screen, "yellow", False, points)




def physics():
  for object in objects:
    object.draw_path()
    object.draw()
    if not object.static:
      for body in objects:
        if body is not object:
          acceleration = object.cal_gravity(body)
          object.vel += acceleration

          object.vel = object.vel.clamp_magnitude(3)

          # print(object.name, object.vel)
          if debug:
            object.draw_line('purple', acceleration, 1000)
      object.pos += object.vel

    if debug:
      object.draw_line('red', object.vel, 30)

def tracking():
  for particle in objects:
    if not particle.static:
      particle.points.append(particle.pos.copy())
      if len(particle.points) > 10:
        particle.points.pop(0)


sun = Particle('sun', pygame.Vector2(0,0), pygame.Vector2(0,0), "white", 400)
sun.freeze()
earth = Particle('earth' ,pygame.Vector2(0,-500), pygame.Vector2(1,0), "green", 20)
moon = Particle('moon', pygame.Vector2(0, -234*2), pygame.Vector2(1.8,0), "gray", 0.01)
mars = Particle('mars', pygame.Vector2(0, 500*2), pygame.Vector2(-0.7,0), "orange", 20)

player = Particle('ship', pygame.Vector2(500*2, 0), pygame.Vector2(0,-0.5), "white", 0.01)
player_rotation = pygame.Vector2(0,-1)
objects = {sun, earth, mars, moon, player}

ONE_SECOND_TIMER = pygame.event.custom_type()
pygame.time.set_timer(ONE_SECOND_TIMER, 1000)

while running:

  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == MOUSEWHEEL:
      global_zoom += event.y * 0.1
      print(global_zoom)
      # if event.y != 0:
      #   window_area = pygame.Vector2(pygame.display.get_window_size())
      #   bottom_right = global_offset + window_area/global_zoom
      #   midpoint = bottom_right/2
      #   global_offset += (midpoint - (midpoint - global_offset) / (1 - (event.y *0.1)))
      #   print(midpoint, global_offset, global_zoom, event.y* 0.1)
    elif event.type == ONE_SECOND_TIMER:
      tracking()

  # fill the screen with a color to wipe away anything from last frame
  screen.fill(BLACK)

  keys = pygame.key.get_pressed()
  if keys[pygame.K_f]:
    pygame.display.toggle_fullscreen()
  if keys[pygame.K_F3]:
    debug = not debug
  if keys[pygame.K_w]:
      player.vel += player_rotation * 0.01
  if keys[pygame.K_a]:
    player_rotation.rotate_ip(-1)
  if keys[pygame.K_d]:
    player_rotation.rotate_ip(1)
  if keys[pygame.K_UP]:
    global_offset.y += speed * global_zoom
  if keys[pygame.K_DOWN]:
    global_offset.y -= speed * global_zoom
  if keys[pygame.K_RIGHT]:
    global_offset.x -= speed * global_zoom
  if keys[pygame.K_LEFT]:
    global_offset.x += speed * global_zoom
  # print(player_rotation)
  pygame.draw.aaline(screen, 'green', (player.pos + global_offset)/global_zoom, (player.pos + global_offset + player_rotation*100)/global_zoom)

  physics()


  pygame.display.flip()
  clock.get_fps()
  clock.tick(60)  # limits FPS to 60
pygame.quit()
