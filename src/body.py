"""Provides a container for bodies to be simulated.

Body acts as a basic object with a position, mass, velocity, and functions for
spatial partitioning and plotting bodies.
"""

import numpy as np
import matplotlib.pyplot as plt


class Body:
    """A body to be simulated.

    Attributes:
        r: 2 element array containing x and y positions of body.
        mass: floating point mass of body.
        v: 2 element array containing velocity of body in x and y directions.
        F: 2 element array containing forces acting on body in x and y directions.

    """
    def __init__(self, x, y, m, vx = 0.0, vy = 0.0) -> None:
        """
        Initializes body with a position, mass, and optional starting velocity.

        :param x: x coordinate of body.
        :param y: y coordinate of body.
        :param m: mass of body.
        :param vx: initial velocity of body in x direction.
        :param vy: initial velocity of body in y direction.
        """
        self.r = np.array([x, y])
        self.v = np.array([vx, vy])
        self.mass = m
        self.force = np.array([0.0, 0.0])

    def in_quad(self, quad):
        """
        Checks if Body is located in a given quad.

        :param quad: the quad to be checked.
        """
        return ((quad.r[0] < self.r[0] and quad.r[0] + quad.length > self.r[0]) and
            (quad.r[1] < self.r[1] and quad.r[1] + quad.length > self.r[1]))


    def plot(self):
        """
        Plots body to the screen.
        """
        plt.scatter(self.r[0], self.r[1], 4.0, 'black')
