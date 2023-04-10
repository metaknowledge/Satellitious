import pygame

class CustomEvents:
  PLAY = pygame.event.custom_type()

  @staticmethod
  def post(event):
    pygame.event.post(pygame.event.Event(event))