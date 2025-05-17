import pygame
from pygame.locals import *

from src.components.game_state import GameState
from src.global_state import GlobalState
from src.game_phase import main_menu, game, settings
from src.services.visualization_service import VisualizationService
from src.services.UI_service import UIService
from src.components.interface_node import InterfaceNode
from src.custom_events import CustomEvents
from src.utils.game_tools import load_planets
from src.utils.tools import add_tuples
from src.components.player import Player

import logging
logging.basicConfig(filename='logs.log',filemode="w", encoding='utf-8', level=logging.DEBUG)



def main():
  # start pygame
  pygame.init()
  GlobalState.load_window()
  screen_sizes = pygame.display.get_desktop_sizes()
  logging.debug(screen_sizes)

  GlobalState.load_user_interface()

  GlobalState.player = Player(pygame.Vector2(21000, 0), "white", 0.1, pygame.Vector2(0, -1), pygame.Vector2(0, -1))

  # game loop
  while GlobalState.running:
    if GlobalState.GAME_STATE == GameState.MAIN_MENU:
      main_menu()
    if GlobalState.GAME_STATE == GameState.SETTINGS:
      settings()
    if GlobalState.GAME_STATE == GameState.GAME:
      game()

    GlobalState.SCREEN.fill("white")

    GlobalState.world_ui.update()
    GlobalState.world_ui.draw(GlobalState.SCREEN)

    GlobalState.update_game_display()


  pygame.quit()



if __name__ == "__main__":
    main()