import pygame
from pygame.locals import *
import logging

def post_quit():
  pygame.event.post(pygame.event.Event(QUIT))
  logging.debug("exit")

def get_screen_sizes():
  return pygame.display.get_desktop_sizes()


def replace_node(group, old_node, new_node):
  group.remove(old_node)
  group.add(new_node)