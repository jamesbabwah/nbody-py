"""Implementation of renderer using pygame.
"""

from typing import override
import pygame as pg

from .abstract_renderer import AbstractRenderer #todo: fix relative import bs


class PGRenderer(AbstractRenderer):
    """Implementation of AbstractRenderer using pygame for plotting visuals.
    """

    def __init__(self, window_len: int,
                 window_height: int,
                 flags: int = 0,
                 depth: int = 0,
                 display: int = 0,
                 vsync: int = 0):
        super().__init__()

        pg.init()
        self.window = pg.display.set_mode((window_len, window_height), flags, depth, display, vsync)
        self.window.fill("black")
    @override
    def draw_grid(self, x, y, length):
        """Uses pygame.draw.rect to draw grids"""
        pg.draw.rect(self.window,
                     pg.Color("green"),
                     pg.Rect(x, y, length, length),
                     2)
    @override
    def draw_body(self, x, y, radius = 2):
        """Uses pygame.draw.circle to draw body"""
        pg.draw.circle(self.window,
                       pg.Color("white"),
                       (x, y),
                       radius)
    @override
    def update(self):
        """Flips the display then draws a black screen for next update.
        Must be called each frame."""
        pg.display.flip()
        self.window.fill("black")
