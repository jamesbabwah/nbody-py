"""Provides Quad and QuadTreeNode classes used for spatial partitioning.

QuadTreeNode is used to construct the Quad Tree which is needed in the Barnes-Hut
algorithm for more efficient computation of forces in the N-body problem.
QuadTreeNode utilizes Quad for keeping the dimensions of each node and subdivision
of nodes.
"""

import numpy as np

from nbody.body import Body
from nbody.renderer.abstract_renderer import AbstractRenderer

class Quad:
    """
    Contains the dimensions of each bounding box for Nodes making up the Quadtree.

    Attributes:
        r: 2D coordinate of lower left corner
        length: side length of quad
    """
    __slots__ = (
        "x1", "x2", "y1", "y2", "length",
        "midx", "midy", "se", "sw", "ne", "nw"
    )
    def __init__(self, x: float, y: float, length: float) -> None:
        """
        Initializes the quad with the location of the South West corner and side length.

        :param rx: x position of left side of quad.
        :param ry: y position of bottom side of quad.
        :param length: length of quad side.
        """
        self.x1, self.x2 = x, x+length
        self.y1, self.y2 = y, y+length
        self.length = length
        self.midx = self.x1 + self.length/2
        self.midy = self.y1 + self.length/2

        self.sw = None
        self.se = None
        self.nw = None
        self.ne = None

    def create_children(self):
        """
        Creates ne, nw, se, and sw quads for subdivision.
        """

        halflength = self.length/2

        self.sw = Quad(self.x1, self.y1, halflength)
        self.se = Quad(self.midx, self.y1, halflength)
        self.nw = Quad(self.x1, self.midy, halflength)
        self.ne = Quad(self.midx, self.midy, halflength)

    def plot(self, renderer: AbstractRenderer):
        """
        Plots the quad to the screen.

        :param renderer: Renderer used for plotting visuals.
        """
        renderer.draw_grid(self.x1, self.y1, self.length)


class QuadTreeNode:
    """
    Used to construct a quadtree.

    Attributes:
        quad: instance of Quad containing the dimensions of the region held by this node.
        body: the body contained in this node, can be None.
        is_leaf: tells if this node is an exterior node.
        mass: sum of masses within this node.
        com: 2 element array containing the position of the centre of mass of this node.
        sw: QuadTreeNode instance representing the South West child of this node.
        se: QuadTreeNode instance representing the South East child of this node.
        nw: QuadTreeNode instance representing the North West child of this node.
        ne: QuadTreeNode instance representing the North East child of this node.
    """
    __slots__ = (
        "quad", "sw", "se", "nw", "ne",
        "body", "is_leaf", "mass", "cx", "cy"
    )

    def __init__(self, quad : Quad) -> None:
        """
        Initializes a quadtree node with the quad dimensions.

        :param quad: the dimensions of the quad of this node.
        """
        self.quad = quad
        self.sw : QuadTreeNode | None = None
        self.se : QuadTreeNode | None = None
        self.nw : QuadTreeNode | None = None
        self.ne : QuadTreeNode | None = None
        self.body : Body | None = None
        self.is_leaf = True

        self.mass = 0.0
        self.cx = 0.0
        self.cy = 0.0

    def insert_body(self, body: Body) -> None:
        """
        Inserts a new body into quadtree.

        Recursively checks if self is an exterior node (leaf) until the deepest node containing
        the body is found then checks if the node is empty. If it is, the body is simply added to
        the node, otherwise the node is subdivided and the new body and body held in node are
        inserted into the corresponding nodes.

        :param body: body to be inserted.
        """
        # update centre of mass
        new_mass = self.mass + body.mass
        self.cx = (self.mass * self.cx + body.mass * body.x)/new_mass
        self.cy = (self.mass * self.cy + body.mass * body.y)/new_mass
        self.mass = new_mass

        if self.is_leaf:
            if self.body is None:
                self.body = body
                return
            else:
                self.subdivide()
                self.findquad(self.body).insert_body(self.body)
                self.body = None

        self.findquad(body).insert_body(body)


    def findquad(self, body: Body):
        """
        Finds the child node of self that body belongs to

        :param body: the body that is to be located in one of the child nodes.
        """
        assert self.sw is not None
        assert self.se is not None
        assert self.ne is not None
        assert self.nw is not None

        if body.x >= self.quad.midx:
            if body.y >= self.quad.midy:
                return self.ne
            else:
                return self.se
        else:
            if body.y >= self.quad.midy:
                return self.nw
            else:
                return self.sw

        # No quad found
        raise RuntimeError("Failed to find quad containing body")

    def subdivide(self) -> None:
        """
        Creates child members of self
        """
        self.is_leaf = False

        self.quad.create_children()
        self.sw = QuadTreeNode(self.quad.sw)
        self.se = QuadTreeNode(self.quad.se)
        self.nw = QuadTreeNode(self.quad.nw)
        self.ne = QuadTreeNode(self.quad.ne)


    def plot(self, renderer: AbstractRenderer, plotquads: bool=False):
        """
        Plots body and (optionally) the bounding box of quads.

        :param renderer: Renderer used for plotting visuals.
        :param plotquads: Defines if quads should be visualised.
        """
        if self.body is not None:
            self.body.plot(renderer)
        if self.is_leaf:
            if plotquads:
                self.quad.plot(renderer)
        else:
            assert self.sw is not None
            assert self.se is not None
            assert self.ne is not None
            assert self.nw is not None
            self.sw.plot(renderer, plotquads)
            self.se.plot(renderer, plotquads)
            self.nw.plot(renderer, plotquads)
            self.ne.plot(renderer, plotquads)
