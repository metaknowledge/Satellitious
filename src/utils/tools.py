import pygame
from pygame.locals import *
import logging
from src.custom_events import CustomEvents

def post_quit():
  pygame.event.post(pygame.event.Event(QUIT))
  logging.debug("exit")

def change_screen_size(size: tuple):
  pygame.display.set_mode(size)
  CustomEvents.post(CustomEvents.CHANGE_SIZE)
  logging.info(size)

def replace_node(group, old_node, new_node):
  group.remove(old_node)
  group.add(new_node)

def add_tuples(a: tuple, b: tuple) -> tuple:
  return list(map(sum, zip(a, b)))