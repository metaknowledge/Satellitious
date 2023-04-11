import pygame

from src.components.game_state import GameState
from src.config import Config

class GlobalState:
  GAME_STATE = GameState.MAIN_MENU
  SCREEN: pygame.Surface = None
  debug = True
  #difference in time since last tick
  delta = 0
  clock: pygame.time.Clock = None
  world_ui = pygame.sprite.Group()
  planets = None
  offset = pygame.Vector2(0,0)
  zoom = 10
  ticks = 0

  @staticmethod
  def load_window():
    GlobalState.SCREEN = pygame.display.set_mode(Config.screen_size)
    GlobalState.SCREEN.fill("black")
    GlobalState.clock = pygame.time.Clock()

  @staticmethod
  def toggle_debug():
    GlobalState.debug = not GlobalState.debug

  @staticmethod
  def update_game_display():
    pygame.display.flip()
    GlobalState.ticks = pygame.time.get_ticks()
    #diffrence of time between each tick in seconds
    GlobalState.delta = GlobalState.clock.tick(60) / 1000


