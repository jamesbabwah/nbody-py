"""Provides Quad and QuadTreeNode classes used for spatial partitioning.

QuadTreeNode is used to construct the Quad Tree which is needed in the Barnes-Hut
algorithm for more efficient computation of forces in the N-body problem.
QuadTreeNode utilizes Quad for keeping the dimensions of each node and subdivision
of nodes.
"""

import matplotlib.pyplot as plt
import numpy as np
from body import Body

class Quad:
    """
    Contains the dimensions of each bounding box for Nodes making up the Quadtree.

    Attributes:
        r: 2D coordinate of lower left corner
        length: side length of quad
    """
    def __init__(self, rx: float, ry: float, length: float) -> None:
        """
        Initializes the quad with the location of the South West corner and side length.

        :param rx: x position of left side of quad.
        :param ry: y position of bottom side of quad.
        :param length: length of quad side.
        """
        self.r = np.array([rx, ry])
        self.length = length

    def plot(self):
        """
        Plots the quad to the screen.
        """
        plt.plot([self.r[0], self.r[0] + self.length],
                 [self.r[1], self.r[1]], 'g')
        plt.plot([self.r[0] + self.length, self.r[0] + self.length],
                 [self.r[1], self.r[1] + self.length], 'g')
        plt.plot([self.r[0], self.r[0]], [self.r[1],
                                          self.r[1] + self.length], 'g')
        plt.plot([self.r[0], self.r[0] + self.length],
                 [self.r[1] + self.length, self.r[1] + self.length], 'g')

    def sw(self):
        """
        Returns South West region of self.
        """
        return Quad(self.r[0], self.r[1], self.length/2.0)
    def se(self):
        """
        Returns South East region of self.
        """
        return Quad(self.r[0] + self.length/2.0, self.r[1], self.length/2.0)
    def nw(self):
        """
        Returns North West region of self.
        """
        return Quad(self.r[0], self.r[1] + self.length/2.0, self.length/2.0)
    def ne(self):
        """
        Returns North East region of self.
        """
        return Quad(self.r[0] + self.length/2.0, self.r[1] + self.length/2.0, self.length/2.0)


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
        self.com = np.array([0, 0])

    def insert_body(self, body: Body) -> None:
        """
        Inserts a new body into quadtree.

        Recursively checks if self is an exterior node (leaf) until the deepest node containing
        the body is found then checks if the node is empty. If it is, the body is simply added to
        the node, otherwise the node is subdivided and the new body and body held in node are
        inserted into the corresponding nodes.

        :param body: body to be inserted.
        """
        if self.is_leaf:
            if self.body is None:
                self.body = body
                self.com = body.r
                self.mass = body.mass
            else:
                self.subdivide()
                self.findquad(self.body).insert_body(self.body)
                self.body = None

                self.findquad(body).insert_body(body)

                self.com = (self.mass * self.com + body.mass * body.r)/(self.mass + body.mass)
                self.mass += body.mass
        else:
            self.findquad(body).insert_body(body)


    def findquad(self, body):
        """
        Finds the child node of self that body belongs to

        :param body: the body that is to be located in one of the child nodes.
        """
        assert self.sw is not None
        assert self.se is not None
        assert self.ne is not None
        assert self.nw is not None

        if body.in_quad(self.sw.quad):
            return self.sw
        if body.in_quad(self.se.quad):
            return self.se
        if body.in_quad(self.nw.quad):
            return self.nw
        if body.in_quad(self.ne.quad):
            return self.ne

        # No quad found
        raise RuntimeError("Insertion of body failed")

    def subdivide(self) -> None:
        """
        Creates child members of self
        """
        self.is_leaf = False
        self.sw = QuadTreeNode(self.quad.sw())
        self.se = QuadTreeNode(self.quad.se())
        self.nw = QuadTreeNode(self.quad.nw())
        self.ne = QuadTreeNode(self.quad.ne())


    def plot(self, plotquads: bool=False):
        """
        Plots body and (optionally) the bounding box of quads.

        :param plotquads: Defines if quads should be visualised.
        """
        if self.body is not None:
            self.body.plot()
        if self.is_leaf:
            if plotquads:
                self.quad.plot()
        else:
            assert self.sw is not None
            assert self.se is not None
            assert self.ne is not None
            assert self.nw is not None
            self.sw.plot(plotquads)
            self.se.plot(plotquads)
            self.nw.plot(plotquads)
            self.ne.plot(plotquads)
