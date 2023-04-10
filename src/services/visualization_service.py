import pygame

from paths import *
from src.components.interface_node import InterfaceNode
from src.utils.tools import post_quit

class VisualizationService:
  @staticmethod
  def change_screen_size(size):
    pygame.display.set_mode(size)

  @staticmethod
  def get_icon_image():
    return pygame.image.load(IMG_DIR / "icon.png")

  @staticmethod
  def get_fira_font():
    return pygame.font.Font(ASSETS_DIR / "fonts" / "FiraCode-Regular.ttf", 40)

  @staticmethod
  def load_main_game_displays():
    pygame.display.set_caption("Asteroids")
    icon = VisualizationService.get_icon_image()
    pygame.display.set_icon(icon)

  #main menu
  @staticmethod
  def get_background() -> InterfaceNode:
    #background
    background = InterfaceNode.from_size(1280, 720)
    background.color = pygame.Color('chocolate')
    title = InterfaceNode.from_surface(VisualizationService.get_fira_font().render('->Asteroids<-', True, 'white', 'chocolate'))
    title.rect.topleft = (50, 50)
    background.add_children(title)
    return background

  def get_menu_buttons() -> InterfaceNode:
    #buttons
    buttons = InterfaceNode.from_size(100, 100)
    buttons.image.fill("purple")
    play_button = InterfaceNode.from_pos_size(0, 0, 100,25)
    play_button.image.fill("red")
    settings_button = InterfaceNode.from_pos_size(0, 25, 100, 26)
    settings_button.image.fill("blue")
    exit_button = InterfaceNode.from_pos_size(0, 51, 100, 27)
    exit_button.image.fill("green")
    exit_button.add_click_event(lambda: post_quit())
    buttons.add_children(play_button, settings_button, exit_button)
    return buttons

  @staticmethod
  def get_settings() -> InterfaceNode:
    #settings
    settings = InterfaceNode.from_size(1280, 720)
    settings.image.fill('orange')
    button_close = InterfaceNode.from_size(50, 50)
    button_close.image.fill('red')
    button_close.rect.topright = tuple(map(sum, zip(settings.rect.topright, (-10, 10))))
    settings.add_children(button_close)
    return settings


