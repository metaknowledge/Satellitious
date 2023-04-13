import pygame
from pygame.locals import *

from src.components.game_state import GameState
from src.global_state import GlobalState
from src.game_phase import main_menu, game
from src.services.visualization_service import VisualizationService
from src.components.interface_node import InterfaceNode
from src.custom_events import CustomEvents
from src.utils.game_tools import load_planets
from src.components.player import Player

import logging
logging.basicConfig(filename='logs.log',filemode="w", encoding='utf-8', level=logging.DEBUG)



def main():
  pygame.init()
  GlobalState.load_window()

  #makes the main menu
  background = VisualizationService.get_background()
  settings = VisualizationService.get_settings()
  menu_buttons = VisualizationService.get_menu_buttons()
  menu_buttons.rect.bottomleft = tuple(map(sum, zip(background.rect.bottomleft, (10, -10))))
  background.add_children(menu_buttons)

  #make the game ui
  game_screen = InterfaceNode.from_size(1180, 620)
  game_screen.rect.topleft = (50,50)
  game_screen.image.fill("black")

  #makes the world ui
  GlobalState.world_ui.add(background)
  close_ui = pygame.sprite.Group()
  close_ui.add(settings)

  #add functionality
  menu_buttons.children.sprites()[1].add_click_event(lambda: background.add_children(settings))
  settings.children.sprites()[0].add_click_event(lambda: background.remove_children(settings))
  menu_buttons.children.sprites()[0].add_click_event(lambda: CustomEvents.post(CustomEvents.PLAY))

  GlobalState.player = Player(pygame.Vector2(20000, 0), "white", 0.1, pygame.Vector2(0, 1), pygame.Vector2(0, 1))

  # menu_buttons.children.sprites()[0].add_click_event(lambda: logging.debug("changed game!"))
  while GlobalState.running:

    if GlobalState.GAME_STATE == GameState.MAIN_MENU:
      main_menu(background, menu_buttons, settings, game_screen)
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