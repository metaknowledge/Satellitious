<<<<<<< HEAD
import pygame

from src.components.particle import Particle
from src.global_state import GlobalState

class Player(Particle):
  vel: pygame.Vector2
  rotation: pygame.Vector2
  mask: pygame.Mask

  def __init__(self, position,  color, objectmass, velocity: pygame.Vector2, rotation: pygame.Vector2):
    super().__init__(position, color, objectmass)
    self.vel = velocity
    self.rotation = rotation

  def update(self, planets) -> pygame.Vector2:
    total_acceleration = pygame.Vector2(0,0)
    for planet in planets:
      acceleration = self.cal_gravity(planet)
      self.vel += acceleration
      total_acceleration += acceleration
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        GlobalState.accelerating = True
        self.vel += self.rotation * 0.01
        total_acceleration = self.rotation * 0.01
    if keys[pygame.K_a]:
      self.rotation.rotate_ip(-3)
    if keys[pygame.K_d]:
      self.rotation.rotate_ip(3)
    return total_acceleration

  def draw_debug(self, screen):
    pygame.draw.aaline(screen, 'green', (self.pos + GlobalState.offset)/GlobalState.zoom, (self.pos + GlobalState.offset)/ GlobalState.zoom + self.rotation*100)
    # mouse_position(pygame.mouse.get_pos())
=======
import pygame

from src.components.particle import Particle
from src.global_state import GlobalState

class Player(Particle):
  vel: pygame.Vector2
  rotation: pygame.Vector2
  mask: pygame.Mask

  def __init__(self, position,  color, objectmass, velocity: pygame.Vector2, rotation: pygame.Vector2):
    super().__init__(position, color, objectmass)
    self.vel = velocity
    self.rotation = rotation


  def update(self, planets) -> pygame.Vector2:
    total_acceleration = pygame.Vector2(0,0)
    for planet in planets:
      acceleration = self.cal_gravity(planet)
      self.vel += acceleration
      total_acceleration += acceleration
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        GlobalState.accelerating = True
        self.vel += self.rotation * 0.01
        total_acceleration = self.rotation * 0.01
    if keys[pygame.K_a]:
      self.rotation.rotate_ip(-3)
    if keys[pygame.K_d]:
      self.rotation.rotate_ip(3)
    return total_acceleration

  def draw_debug(self, screen):
    pygame.draw.aaline(screen, 'green', (self.pos + GlobalState.offset)/GlobalState.zoom, (self.pos + GlobalState.offset)/ GlobalState.zoom + self.rotation*100)
    # mouse_position(pygame.mouse.get_pos())
>>>>>>> caa9f23c1f0a44c7ce068ce12609939477b9d911
