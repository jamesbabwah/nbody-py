"""Provides QuadTreeNode class used for spatial partitioning.

QuadTreeNode is used to construct the Quad Tree which is needed in the Barnes-Hut
algorithm for more efficient computation of forces in the N-body problem.
"""

from nbody.body import Body
from nbody.renderer.abstract_renderer import AbstractRenderer


class QuadTreeNode:
    """
    Used to construct a quadtree.

    Attributes:
        x1: x position of left side
        x2: x position of right side
        y1: y position of bottom side
        y2: y position of top side
        length: side length of node
        body: the body contained in this node, can be None.
        is_leaf: tells if this node is an exterior node.
        mass: sum of masses within this node.
        cx: x position of center of mass of this node
        cy: y position of center of mass of this node
        sw: QuadTreeNode instance representing the South West child of this node.
        se: QuadTreeNode instance representing the South East child of this node.
        nw: QuadTreeNode instance representing the North West child of this node.
        ne: QuadTreeNode instance representing the North East child of this node.
    """
    __slots__ = (
        "x1", "x2", "y1", "y2", "length",
        "sw", "se", "nw", "ne",
        "body", "is_leaf", "mass", "cx", "cy"
    )

    def __init__(self, x: float, y: float, length: float) -> None:
        """
        Initializes a quadtree node with the quad dimensions.

        :param x: the x coordinate of the bottom left corner
        :param y: the y coordinate of the bottom left corner
        :param length: the length of the side of the quad
        """

        self.x1, self.x2 = x, x+length
        self.y1, self.y2 = y, y+length
        self.length = length
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
        m = self.mass
        bm = body.mass
        x = body.x
        y = body.y
        new_mass = m + bm
        self.cx = (m * self.cx + bm * x)/new_mass
        self.cy = (m * self.cy + bm * y)/new_mass
        self.mass = new_mass

        midx = (self.x1 + self.x2)/2
        midy = (self.y1 + self.y2)/2
        if self.is_leaf:
            if self.body is None:
                self.body = body
                return
            else:
                self.subdivide()
                if self.body.x >= midx:
                    if self.body.y >= midy:
                        self.ne.insert_body(self.body)
                    else:
                        self.se.insert_body(self.body)
                else:
                    if self.body.y >= midy:
                        self.nw.insert_body(self.body)
                    else:
                        self.sw.insert_body(self.body)
                self.body = None

        if body.x >= midx:
            if body.y >= midy:
                self.ne.insert_body(body)
            else:
                self.se.insert_body(body)
        else:
            if body.y >= midy:
                self.nw.insert_body(body)
            else:
                self.sw.insert_body(body)


    def findquad(self, body: Body):
        """
        Finds the child node of self that body belongs to

        :param body: the body that is to be located in one of the child nodes.
        """
        assert self.sw is not None
        assert self.se is not None
        assert self.ne is not None
        assert self.nw is not None

        midx = (self.x1 + self.x2)/2
        midy = (self.y1 + self.y2)/2
        if body.x >= midx:
            if body.y >= midy:
                return self.ne
            else:
                return self.se
        else:
            if body.y >= midy:
                return self.nw
            else:
                return self.sw

        # No quad found
        raise RuntimeError("Failed to find quad containing body")

    def subdivide(self) -> None:
        """
        Creates child nodes of self
        """
        self.is_leaf = False

        halflength = self.length/2
        midx = (self.x1 + self.x2)/2
        midy = (self.y1 + self.y2)/2
        self.sw = QuadTreeNode(self.x1, self.y1, halflength)
        self.se = QuadTreeNode(midx, self.y1, halflength)
        self.nw = QuadTreeNode(self.x1, midy, halflength)
        self.ne = QuadTreeNode(midx, midy, halflength)


    def plot(self, renderer: AbstractRenderer, plotquads: bool=False):
        """
        Plots body and (optionally) the bounding box of quads.

        :param renderer: Renderer used for plotting visuals.
        :param plotquads: Defines if bounding boxes should be visualised.
        """
        if self.body is not None:
            self.body.plot(renderer)
        if self.is_leaf:
            if plotquads:
                renderer.draw_grid(self.x1, self.y1, self.length)
        else:
            assert self.sw is not None
            assert self.se is not None
            assert self.ne is not None
            assert self.nw is not None
            self.sw.plot(renderer, plotquads)
            self.se.plot(renderer, plotquads)
            self.nw.plot(renderer, plotquads)
            self.ne.plot(renderer, plotquads)
