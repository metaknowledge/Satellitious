import pygame

from src.components.game_state import GameState
from src.services.visualization_service import VisualizationService
from src.config import Config
from src.components.interface_node import InterfaceNode

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
  zoom = 1
  ticks = 0
  running = True
  focus = False
  player = None
  main_menu_screen: InterfaceNode
  game_screen: InterfaceNode
  settings_screen: InterfaceNode

  @staticmethod
  def load_window():
    GlobalState.SCREEN = pygame.display.set_mode(Config.screen_size)
    GlobalState.SCREEN.fill("black")
    GlobalState.clock = pygame.time.Clock()
    pygame.display.set_caption("Satellitious")
    icon = VisualizationService.get_icon_image()
    pygame.display.set_icon(icon)

  @staticmethod
  def toggle_debug():
    GlobalState.debug = not GlobalState.debug

  @staticmethod
  def update_game_display():
    pygame.display.flip()
    GlobalState.ticks = pygame.time.get_ticks()
    #diffrence of time between each tick in seconds
    GlobalState.delta = GlobalState.clock.tick(Config.FPS) / 1000

  @staticmethod
  def true_position(point: pygame.Vector2):
    return (point + GlobalState.offset) / GlobalState.zoom


