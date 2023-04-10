import pygame
from pygame.locals import *

from src.components.game_state import GameState
from src.global_state import GlobalState
from src.game_phase import main_menu, game
from src.services.visualization_service import VisualizationService
from src.components.interface_node import InterfaceNode
from src.utils.tools import replace_node
from src.custom_events import CustomEvents

import logging
logging.basicConfig(filename='logs.log',filemode="w", encoding='utf-8', level=logging.DEBUG)

def main():

  pygame.init()
  GlobalState.load_window()
  GlobalState.clock = pygame.time.Clock()
  running = True

  #makes the main menu
  background = VisualizationService.get_background()
  settings = VisualizationService.get_settings()
  menu_buttons = VisualizationService.get_menu_buttons()
  menu_buttons.rect.bottomleft = tuple(map(sum, zip(background.rect.bottomleft, (10, -10))))
  background.add_children(menu_buttons)

  #make the game ui
  game_screen = InterfaceNode.from_size(1280, 720)
  game_screen.image.fill("black")

  #makes the world ui
  GlobalState.world_ui.add(background)
  close_ui = pygame.sprite.Group()
  close_ui.add(settings)

  #add functionality
  menu_buttons.children.sprites()[1].add_click_event(lambda: background.add_children(settings))
  settings.children.sprites()[0].add_click_event(lambda: background.remove_children(settings))
  menu_buttons.children.sprites()[0].add_click_event(lambda: pygame.event.post(CustomEvents.PLAY))

  while running:

    #process all events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONUP:
        if GlobalState.GAME_STATE == GameState.MAIN_MENU:
          menu_buttons.collide_with_mouse(pygame.Vector2(event.pos))
          settings.collide_with_mouse(pygame.Vector2(event.pos))
      if event.type == CustomEvents.PLAY:
        replace_node(GlobalState.world_ui, background, game)
        GlobalState.GAME_STATE = GameState.GAME


    if GlobalState.GAME_STATE == GameState.MAIN_MENU:
      main_menu()
    if GlobalState.GAME_STATE == GameState.GAME:
      game(game_screen)

    GlobalState.SCREEN.fill("black")
    GlobalState.world_ui.update()
    GlobalState.world_ui.draw(GlobalState.SCREEN)

    GlobalState.update_game_display()


  pygame.quit()



if __name__ == "__main__":
    main()