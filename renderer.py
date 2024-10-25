from enum import Enum
import pygame

class RGB(Enum):
  YELLOW = (220, 200, 0)
  GREEN = (0, 150, 0)
  RED = (255, 0, 0)
  BLUE = (80, 80, 255)

class Renderer:
  def __init__(self, pixel_size, board_width):
    self.px = pixel_size
    self.board_width = board_width

  def draw_square(self, screen, x, y, colour):
      if isinstance(colour, RGB):
        colour = colour.value
      pygame.draw.rect(screen, colour, (x * self.px, y * self.px, self.px, self.px))

  def draw_text(self, screen, x, y, text, colour):
      font = pygame.font.SysFont("Arial", self.px)
      if isinstance(colour, RGB):
        colour = colour.value
      text = font.render(text, True, colour)
      screen.blit(text, (x * self.px + 4, y * self.px))