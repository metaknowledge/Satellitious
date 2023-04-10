import pygame

from src.components.game_state import GameState
from src.config import Config

class GlobalState:
  GAME_STATE = GameState.MAIN_MENU
  SCREEN: pygame.Surface = None
  debug = True
  #difference in time since last tick
  delta = 0
  clock = None
  world_ui = pygame.sprite.Group()


  @staticmethod
  def load_window():
    GlobalState.SCREEN = pygame.display.set_mode(Config.screen_size)
    GlobalState.SCREEN.fill("black")

  @staticmethod
  def toggle_debug():
    GlobalState.debug = not GlobalState.debug

  @staticmethod
  def update_game_display():
    pygame.display.flip()
    #diffrence of time between each tick in seconds
    GlobalState.delta = GlobalState.clock.tick(60) / 1000


