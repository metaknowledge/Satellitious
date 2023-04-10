import pygame
from pygame.locals import *
from src.components.particle import Particle
from src.game_phase import load_planets

screen = Game.screen

clock = pygame.time.Clock()
running = True
speed = 1

x_axis = pygame.Vector2(1,0)

particles = load_planets()

def physics():
  for particle in particles:
    particle.draw(Game)
    particle.pos += particle.vel
    if not particle.static:
      for body in particles:
        if body is not particle:
          acceleration = particle.cal_gravity(body)
          particle.vel += acceleration
          particle.vel = particle.vel.clamp_magnitude(5)
          if Game.debug:
            particle.draw_line('purple', acceleration, 1000, Game)

      if Game.debug:
        particle.draw_line('red', particle.vel, 30, Game)
        particle.draw_path(Game)

def collisions(planets):
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


def tracking():
  for particle in particles:
    if not particle.static:
      particle.points.append(particle.pos.copy())
      if len(particle.points) > 20:
        particle.points.pop(0)

def post_quit():
  pygame.event.post(pygame.event.Event(QUIT))

def toggle_debug(key):
  Game.debug = not Game.debug

def change_screen_size(key):
  Game.screen_size = (1 + Game.screen_size) % len(Game.screen_sizes)
  pygame.display.set_mode(Game.screen_sizes[Game.screen_size])

def mouse_position(pos):
  pygame.draw.circle(screen, 'white', pos, 1)
  screen.blit(Game.fira_code.render(str(pos), True, "white"), pos)

pygame.mouse.set_visible(False)
key_subs = {'f': [pygame.display.toggle_fullscreen],
            'q': [post_quit],
            '': {
              '1073741884': [toggle_debug],
              '1073741888': [change_screen_size]
              },
            'p': [],
            'a':[],
            's':[],
            'd':[]
            }

ONE_SECOND_TIMER = pygame.event.custom_type()
pygame.time.set_timer(ONE_SECOND_TIMER, 5000)

while running:

  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == MOUSEWHEEL:
      Game.zoom += event.y * 0.01 * Game.zoom
      # if event.y != 0:
      #   window_area = pygame.Vector2(pygame.display.get_window_size())
      #   bottom_right = windowPostion.offset + window_area/windowPostion.zoom
      #   midpoint = bottom_right/2
      #   windowPostion.offset += (midpoint - (midpoint - windowPostion.offset) / (1 - (event.y *0.1)))
      #   print(midpoint, windowPostion.offset, windowPostion.zoom, event.y* 0.1)
    # elif event.type == KEYDOWN:
    #   if event.unicode == '' and str(event.key) in key_subs[event.unicode]:
    #     for func in key_subs[event.unicode][str(event.key)]:
    #       func(event.key)
    #   elif event.unicode != '' and event.unicode in key_subs:
    #     for func in key_subs[event.unicode]:
    #       func()
    # elif event.type == ONE_SECOND_TIMER:
    #   tracking()

  # fill the screen with a color to wipe away anything from last frame
  screen.fill("black")

  if player and Game.debug:
    pygame.draw.aaline(screen, 'green', (player.pos + Game.offset)/Game.zoom, (player.pos + Game.offset + playerRotation*100)/Game.zoom)
    mouse_position(pygame.mouse.get_pos())
    fps = Game.fira_code.render('fps:' + str(clock.get_fps().__trunc__()), True, "white")
    screen.blit(fps, (0,0))

  collisions(particles)
  physics()


  pygame.display.flip()
  clock.tick(60)  # limits FPS to 60
pygame.quit()