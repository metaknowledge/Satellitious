import pygame
from typing import Callable, Self
# from src.components.interface_node import InterfaceNode

class InterfaceNode(pygame.sprite.Sprite):
  image: pygame.Surface
  rect: pygame.Rect
  children: pygame.sprite.Group
  click_event: Callable
  color: pygame.Color
  relative_pos: pygame.Vector2

  def __init__(self, surface, x, y):
    super().__init__()
    self.image = surface
    self.rect = self.image.get_rect(topleft=(x,y))
    self.children = pygame.sprite.Group()
    self.relative_pos = pygame.Vector2(0, 0)
  @classmethod
  def from_pos_size(cls, x, y, w, h):
    return cls(pygame.Surface((w, h)), x, y)

  @classmethod
  def from_surface(cls, surface):
    return cls(surface, 0, 0)

  @classmethod
  def from_size(cls, w, h):
    return cls.from_pos_size(0, 0, w, h)

  @classmethod
  def from_tuple(cls, size: tuple):
    return cls.from_pos_size(0, 0, size[0], size[1])

  def add_children(self, *children):
    for child in children:
      child.set_relative_position(self)
    self.children.add(children)

  def set_relative_position(self, parent: Self):
    self.relative_pos = parent.rect.topleft

  def remove_children(self, *children):
    self.children.remove(children)

  def update(self) -> None:
    self.children.update()
    self.children.draw(self.image)

class Button(InterfaceNode):
  click_event: Callable

  def add_click_event(self, click_event):
    self.click_event = click_event

  def collide_with_mouse(self, mouse_pos: pygame.Vector2):
    relative_mouse_pos = mouse_pos - self.relative_pos
    if self.rect.collidepoint(relative_mouse_pos) and self.click_event:
      self.click_event()


