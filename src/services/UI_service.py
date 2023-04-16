import pygame

from paths import *
from src.services.visualization_service import VisualizationService
from src.components.interface_node import InterfaceNode, Button
from src.utils.tools import post_quit, change_screen_size

class UIService:
  #main menu
  @staticmethod
  def get_background(screen_size: tuple) -> InterfaceNode:
    #background
    background_img = VisualizationService.get_background_img()
    background = InterfaceNode.from_tuple(screen_size)
    background.image.fill("black")
    background.image.blit(background_img, (10, 10))
    return background

  @staticmethod
  def get_title() -> InterfaceNode:
    title = InterfaceNode.from_surface(VisualizationService.get_fira_font(40).render('->Satellitious<-', True, 'white', 'black'))
    title.rect.topleft = (50, 50)
    return title

  def get_menu() -> InterfaceNode:
    #buttons
    buttons = InterfaceNode.from_size(100, 100)
    buttons.image.fill("black")
    return buttons

  @staticmethod
  def get_menu_button() -> Button:
    button = pygame.transform.scale(VisualizationService.get_button_four(), (100,25))
    button = Button.from_surface(button)
    return button

  @staticmethod
  def get_settings(screen_size) -> InterfaceNode:
    #settings
    settings = InterfaceNode.from_tuple(screen_size)
    settings.image.fill('blue')
    return settings

  @staticmethod
  def get_settings_close_button() -> Button:
    button_close = Button.from_surface(VisualizationService.get_fira_font(40).render("EXIT", True, "black", "red"))
    return button_close

  def get_screen_size_buttons(screen_size: pygame.Surface, screen_sizes: list[tuple]) -> InterfaceNode:
    screen_width = screen_size()[0]
    screen_buttons = InterfaceNode.from_pos_size(0, 200,screen_width, 100)
    for i, screen in enumerate(screen_sizes):
      text = VisualizationService.get_fira_font(20).render(str(screen), True, "white", "black")
      text = pygame.transform.scale(text, (screen_width/len(screen_sizes), text.get_size()[1]))
      screen_button = Button.from_surface(text)
      screen_button.rect.topleft = ((screen_width/len(screen_sizes)) * i, 10)
      screen_button.add_click_event(lambda: change_screen_size(screen))
      screen_buttons.add_children(screen_button)



