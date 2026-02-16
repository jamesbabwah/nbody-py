"""Provides renderer interface for drawing to the screen.
"""
from abc import ABC, abstractmethod


class AbstractRenderer(ABC):
    """Abstract interface for rendering bodies and quadtree.
    """

    @abstractmethod
    def draw_grid(self, x: int, y: int, length: int) -> None:
        """Draws the bounding box of a quadtree node.

        :param quad: the node being drawn.
        """

    @abstractmethod
    def draw_body(self, x: int, y: int, radius: int = 1) -> None:
        """Draws a body to the screen.

        :param body: the body being drawn.
        """

    @abstractmethod
    def update(self) -> None:
        """
        Updates the display.
        """
