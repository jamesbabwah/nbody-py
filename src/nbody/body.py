"""Provides a container for bodies to be simulated.

Body acts as a basic object with a position, mass, velocity, and functions for
spatial partitioning and plotting bodies.
"""

import numpy as np
from nbody.renderer.abstract_renderer import AbstractRenderer


class Body:
    """A body to be simulated.

    Attributes:
        x: x position of body
        y: y position of body
        r: np.array([x,y])
        mass: floating point mass of body.
        v: 2 element array containing velocity of body in x and y directions.
        F: 2 element array containing forces acting on body in x and y directions.

    """
    def __init__(self, x, y, m, *, vx = 0.0, vy = 0.0) -> None:
        """
        Initializes body with a position, mass, and optional starting velocity.

        :param x: x coordinate of body.
        :param y: y coordinate of body.
        :param m: mass of body.
        :param vx: initial velocity of body in x direction.
        :param vy: initial velocity of body in y direction.
        """
        self.r = np.array([x, y])
        self.x = x
        self.y = y
        self.v = np.array([vx, vy])
        self.mass = m
        self.force = np.array([0.0, 0.0])

    def plot(self, renderer: AbstractRenderer):
        """
        Plots body to the screen.

        :param renderer: Renderer used for plotting visuals.
        """
        renderer.draw_body(self.r[0], self.r[1])
