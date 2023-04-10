import pygame
from typing import Callable
# from src.components.interface_node import InterfaceNode

class InterfaceNode(pygame.sprite.Sprite):
  image: pygame.Surface
  rect: pygame.Rect
  children: pygame.sprite.Group
  click_event: Callable
  color: pygame.Color

  def __init__(self, surface, x, y, click_event, color):
    super().__init__()
    self.image = surface
    self.rect = self.image.get_rect(topleft=(x,y))
    self.children = pygame.sprite.Group()
    self.click_event = click_event
    self.color = color

  @classmethod
  def from_pos_size(cls, x, y, w, h):
    return cls(pygame.Surface((w, h)), x, y, None, None)

  @classmethod
  def from_surface(cls, surface):
    return cls(surface, 0, 0, None, None)

  @classmethod
  def from_size(cls, w, h):
    return cls.from_pos_size(0, 0, w, h)

  def add_children(self, *children):
    self.children.add(children)

  def remove_children(self, *children):
    self.children.remove(children)

  def add_click_event(self, click_event):
    self.click_event = click_event

  def update(self) -> None:
    if self.color:
      self.image.fill(self.color)
    self.children.update()
    self.children.draw(self.image)

  def collide_with_mouse(self, mouse_pos: pygame.Vector2):
    for node in self.children.sprites():
      relative_mouse_pos = mouse_pos - pygame.Vector2(self.rect.topleft)
      if node.rect.collidepoint(relative_mouse_pos) and node.click_event:
        node.click_event()

  @staticmethod
  def remove_from_group(group: pygame.sprite.Sprite, node):
    group.remove(node)