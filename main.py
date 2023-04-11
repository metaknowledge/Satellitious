import pygame
from pygame.locals import *

from src.components.game_state import GameState
from src.global_state import GlobalState
from src.game_phase import main_menu, game
from src.services.visualization_service import VisualizationService
from src.components.interface_node import InterfaceNode
from src.utils.tools import replace_node
from src.custom_events import CustomEvents
from src.utils.game_tools import load_planets


import logging
logging.basicConfig(filename='logs.log',filemode="w", encoding='utf-8', level=logging.DEBUG)

def main():

  pygame.init()
  GlobalState.load_window()
  running = True

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

  player = None

  fira_font = VisualizationService.get_fira_font()
  # menu_buttons.children.sprites()[0].add_click_event(lambda: logging.debug("changed game!"))
  while running:

    #process all events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        print(event.type)
        running = False
      if event.type == pygame.MOUSEBUTTONUP:
        if GlobalState.GAME_STATE == GameState.MAIN_MENU:
          menu_buttons.collide_with_mouse(pygame.Vector2(event.pos))
          settings.collide_with_mouse(pygame.Vector2(event.pos))
      if event.type == CustomEvents.PLAY:
        replace_node(GlobalState.world_ui, background, game_screen)
        GlobalState.GAME_STATE = GameState.GAME
        GlobalState.planets = load_planets()
        logging.debug("changed game!")
      if event.type == pygame.MOUSEWHEEL:
        GlobalState.zoom += event.y * 0.01 * GlobalState.zoom

    if GlobalState.GAME_STATE == GameState.MAIN_MENU:
      main_menu()
    if GlobalState.GAME_STATE == GameState.GAME:
      game(game_screen.image)
      keys = pygame.key.get_pressed()
      if keys[pygame.K_UP]:
        GlobalState.offset.y += GlobalState.zoom * GlobalState.delta * 1000
      if keys[pygame.K_DOWN]:
        GlobalState.offset.y -= GlobalState.zoom * GlobalState.delta * 1000
      if keys[pygame.K_RIGHT]:
        GlobalState.offset.x -= GlobalState.zoom * GlobalState.delta * 1000
      if keys[pygame.K_LEFT]:
        GlobalState.offset.x += GlobalState.zoom * GlobalState.delta * 1000
      # player.update()
      if player and GlobalState.debug:
        player.draw_debug(game_screen.image)
        fps = fira_font.render('fps:' + str(GlobalState.clock.get_fps().__trunc__()), True, "white")
        game_screen.image.blit(fps, (0,0))

    GlobalState.SCREEN.fill("white")

    GlobalState.world_ui.update()
    GlobalState.world_ui.draw(GlobalState.SCREEN)

    GlobalState.update_game_display()


  pygame.quit()



if __name__ == "__main__":
    main()