import pygame

class CustomEvents:
  PLAY = pygame.event.custom_type()
  CHANGE_SIZE = pygame.event.custom_type()
  SETTINGS = pygame.event.custom_type()

  @staticmethod
  def post(event):
    pygame.event.post(pygame.event.Event(event))