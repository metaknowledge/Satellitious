import pygame
from pygame.locals import *

from src.components.game_state import GameState
from src.global_state import GlobalState
from src.game_phase import main_menu, game
from src.services.visualization_service import VisualizationService
from src.services.UI_service import UIService
from src.components.interface_node import InterfaceNode
from src.custom_events import CustomEvents
from src.utils.game_tools import load_planets
from src.utils.tools import get_screen_sizes, add_tuples
from src.components.player import Player

import logging
logging.basicConfig(filename='logs.log',filemode="w", encoding='utf-8', level=logging.DEBUG)



def main():
  pygame.init()
  GlobalState.load_window()

  screen_sizes = get_screen_sizes()
  logging.debug(screen_sizes)
  #make the game ui
  #makes the main menu
  background: InterfaceNode = UIService.get_background(GlobalState.SCREEN.get_size())
  title = UIService.get_title()
  #three buttons
  menu_buttons = UIService.get_menu()
  menu_buttons.rect.bottomleft = add_tuples(background.rect.bottomleft, (10, -10))
  play_button = UIService.get_menu_button()
  settings_button = UIService.get_menu_button()
  settings_button.rect.topleft = (0, 30)
  exit_button = UIService.get_menu_button()
  exit_button.rect.topleft = (0, 60)
  menu_buttons.add_children(play_button, settings_button, exit_button)

  background.add_children(title, menu_buttons)


  #settings page
  settings: InterfaceNode = UIService.get_settings(GlobalState.SCREEN.get_size())
  close_settings_button = UIService.get_settings_close_button()
  close_settings_button.rect.topright = add_tuples(settings.rect.topright, (-10, -10))
  settings.add_children(close_settings_button)

  #game screen
  game_screen = InterfaceNode.from_size(1280, 720)
  # game_screen.rect.topleft = (50,50)

  #makes the world ui
  GlobalState.world_ui.add(background)
  GlobalState.main_menu_screen = background
  GlobalState.game_screen = game_screen
  GlobalState.settings_screen = settings
  #add functionality
  # menu_buttons.children.sprites()[1].add_click_event(lambda: background.add_children(settings))
  # settings.children.sprites()[0].add_click_event(lambda: background.remove_children(settings))
  # menu_buttons.children.sprites()[0].add_click_event(lambda: CustomEvents.post(CustomEvents.PLAY))
  play_button.add_click_event(lambda: CustomEvents.post(CustomEvents.PLAY))
  settings_button.add_click_event(lambda: CustomEvents.post(CustomEvents.SETTINGS))
  exit_button.add_click_event(lambda: CustomEvents.post(QUIT))

  GlobalState.player = Player(pygame.Vector2(20000, 0), "white", 0.1, pygame.Vector2(0, 1), pygame.Vector2(0, 1))



  # menu_buttons.children.sprites()[0].add_click_event(lambda: logging.debug("changed game!"))
  while GlobalState.running:

    if GlobalState.GAME_STATE == GameState.MAIN_MENU:
      main_menu(menu_buttons)
    if GlobalState.GAME_STATE == GameState.GAME:
      game(game_screen.image)
      # player.update()

    GlobalState.SCREEN.fill("white")

    GlobalState.world_ui.update()
    GlobalState.world_ui.draw(GlobalState.SCREEN)

    GlobalState.update_game_display()


  pygame.quit()



if __name__ == "__main__":
    main()