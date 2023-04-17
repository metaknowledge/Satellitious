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
    title = InterfaceNode.from_surface(VisualizationService.get_boxy_font(40).render('->Satellitious<-', True, 'white', 'black'))
    title.rect.topleft = (50, 50)
    return title

  def get_menu() -> InterfaceNode:
    #buttons
    buttons = InterfaceNode.from_size(200, 100)
    buttons.image.fill("black")
    return buttons

  @staticmethod
  def get_menu_button(text) -> Button:
    button = VisualizationService.get_boxy_font(20).render(text, True, "white", "black")
    button = Button.from_surface(button)
    return button

  @staticmethod
  def get_settings(screen_size) -> InterfaceNode:
    #settings
    settings = InterfaceNode.from_tuple(screen_size)
    settings.image.fill('black')
    return settings

  @staticmethod
  def get_settings_close_button() -> Button:
    button_close = Button.from_surface(VisualizationService.get_boxy_font(40).render("EXIT", True, "white", "black"))
    return button_close

  @staticmethod
  def get_screen_fullscreen_toggle() -> Button:
    fullscreen_button = Button.from_surface(VisualizationService.get_boxy_font(40).render("Fullscreen", True, "white", "black"))
    fullscreen_button.rect.topleft= (10, 10)
    fullscreen_button.add_click_event(pygame.display.toggle_fullscreen)
    return fullscreen_button

  @staticmethod
  def get_fps_button(fps) -> Button:
    fps_button = Button.from_surface(VisualizationService.get_boxy_font(40).render("max fps: " + str(fps), True, "white", "black"))
    fps_button.rect.topleft = (10, 100)
    return fps_button

