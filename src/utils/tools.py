<<<<<<< HEAD
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

# replaces old_node with new_node in group
def replace_node(group, old_node, new_node):
  group.remove(old_node)
  group.add(new_node)

def add_tuples(a: tuple, b: tuple) -> tuple:
=======
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
>>>>>>> caa9f23c1f0a44c7ce068ce12609939477b9d911
  return list(map(sum, zip(a, b)))