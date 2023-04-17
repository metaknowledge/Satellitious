import pygame
from pygame.locals import *

from src.components.game_state import GameState
from src.services.visualization_service import VisualizationService
from src.config import Config
from src.components.interface_node import InterfaceNode
from src.services.UI_service import UIService
from src.utils.tools import add_tuples
from src.custom_events import CustomEvents
from src.components.player import Player

import logging

class GlobalState:
  GAME_STATE = GameState.MAIN_MENU
  SCREEN: pygame.Surface = None
  debug = True
  #difference in time since last tick
  delta = 0
  clock: pygame.time.Clock = None
  world_ui = pygame.sprite.Group()
  menu_buttons = pygame.sprite.Group()
  game_buttons = pygame.sprite.Group()
  settings_buttons = pygame.sprite.Group()
  planets = None
  offset = pygame.Vector2(0,0)
  zoom = 1
  ticks = 0
  running = True
  focus = False
  player: Player = None
  main_menu_screen: InterfaceNode
  game_screen: InterfaceNode
  settings_screen: InterfaceNode
  space_map: pygame.Surface
  hidden_map = False


  @staticmethod
  def load_window():
    GlobalState.SCREEN = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
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

  @staticmethod
  def load_user_interface():
    #make the game ui
    #makes the main menu
    GlobalState.load_main_menu()

    #settings page
    settings_screen = UIService.get_settings(GlobalState.SCREEN.get_size())
    close_settings_button = UIService.get_settings_close_button()
    close_settings_button.rect.topright = add_tuples(settings_screen.rect.topright, (-10, 10))
    close_settings_button.add_click_event(lambda: CustomEvents.post(CustomEvents.MENU))

    fullscreen_button = UIService.get_screen_fullscreen_toggle()

    fps_button = UIService.get_fps_button(Config.FPS)
    fps_button.add_click_event(lambda: Config.increase_FPS())

    settings_screen.add_children(close_settings_button, fullscreen_button, fps_button)
    GlobalState.settings_buttons.add(close_settings_button, fullscreen_button, fps_button)

    #makes the world ui
    GlobalState.game_screen = InterfaceNode.from_tuple(GlobalState.SCREEN.get_size(),)
    GlobalState.space_map = pygame.surface.Surface(add_tuples(GlobalState.SCREEN.get_size(), (-100, -100)))
    GlobalState.settings_screen = settings_screen

    GlobalState.world_ui.add(GlobalState.main_menu_screen)

  @staticmethod
  def load_main_menu():
    background: InterfaceNode = UIService.get_background(GlobalState.SCREEN.get_size())
    title = UIService.get_title()

    #three buttons
    menu_buttons = UIService.get_menu()
    menu_buttons.rect.bottomleft = add_tuples(background.rect.bottomleft, (10, -10))
    play_button = UIService.get_menu_button("Play")
    settings_button = UIService.get_menu_button("Settings")
    settings_button.rect.topleft = (0, 30)
    exit_button = UIService.get_menu_button("Quit")
    exit_button.rect.topleft = (0, 60)
    menu_buttons.add_children(play_button, settings_button, exit_button)
    GlobalState.menu_buttons.add(play_button, settings_button, exit_button)
    play_button.add_click_event(lambda: CustomEvents.post(CustomEvents.PLAY))
    settings_button.add_click_event(lambda: CustomEvents.post(CustomEvents.SETTINGS))
    exit_button.add_click_event(lambda: CustomEvents.post(QUIT))
    background.add_children(title, menu_buttons)

    GlobalState.main_menu_screen = background