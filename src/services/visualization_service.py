import pygame

from paths import *
from src.components.interface_node import InterfaceNode, Button
from src.utils.tools import post_quit,change_screen_size

class VisualizationService:
  #IMAGES
  @staticmethod
  def change_screen_size(size):
    pygame.display.set_mode(size)

  @staticmethod
  def get_icon_image():
    return pygame.image.load(IMG_DIR / "icon.png")

  @staticmethod
  def get_button_five():
    return pygame.image.load(IMG_DIR / "buttons" / "Button_White (5).png")

  @staticmethod
  def get_button_four():
    return pygame.image.load(IMG_DIR / "buttons" / "Button_White (4).png")

  @staticmethod
  def get_background_img():
    return pygame.image.load(IMG_DIR / "background.PNG")

  @staticmethod
  def get_asteroid_img_two():
    return pygame.image.load(IMG_DIR / "asteroidOne.png")

  @staticmethod
  def get_asteroid_img_one():
    return pygame.image.load(IMG_DIR / "asteroidTwo.png")

  #FONTS
  @staticmethod
  def get_boxy_font(font_size):
    return pygame.font.Font(ASSETS_DIR / "fonts" / "Boxy-Bold.ttf", font_size)

  @staticmethod
  def get_fira_font(font_size: int):
    return pygame.font.Font(ASSETS_DIR / "fonts" / "FiraCode-Regular.ttf", font_size)

  #OTHER
  @staticmethod
  def load_icon():
    pygame.display.set_caption("Asteroids")
    icon = VisualizationService.get_icon_image()
    pygame.display.set_icon(icon)