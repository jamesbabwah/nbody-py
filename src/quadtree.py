import matplotlib.pyplot as plt
import numpy as np
from body import Body

class Quad:
    """
    Contains the dimensions of each bounding box for Nodes making up the Quadtree
    """
    def __init__(self, rx: float, ry: float, length: float) -> None:
        self.r = np.array([rx, ry])
        self.length = length

    def plot(self):
        plt.plot([self.r[0], self.r[0] + self.length], [self.r[1], self.r[1]], 'g')
        plt.plot([self.r[0] + self.length, self.r[0] + self.length], [self.r[1], self.r[1] + self.length], 'g')
        plt.plot([self.r[0], self.r[0]], [self.r[1], self.r[1] + self.length], 'g')
        plt.plot([self.r[0], self.r[0] + self.length], [self.r[1] + self.length, self.r[1] + self.length], 'g')

    def sw(self):
        return Quad(self.r[0], self.r[1], self.length/2.0)
    def SE(self):
        return Quad(self.r[0] + self.length/2.0, self.r[1], self.length/2.0)
    def NW(self):
        return Quad(self.r[0], self.r[1] + self.length/2.0, self.length/2.0)
    def NE(self):
        return Quad(self.r[0] + self.length/2.0, self.r[1] + self.length/2.0, self.length/2.0)


class Node:
    def __init__(self, quad : Quad) -> None:
        self.quad = quad
        self.sw : Node | None = None
        self.se : Node | None = None
        self.nw : Node | None = None
        self.ne : Node | None = None
        self.body : Body | None = None
        self.is_leaf = True

        self.mass = 0.0
        self.com = np.array([0, 0])

    def insert_body(self, body: Body) -> None:
        if self.is_leaf:
            if self.body is None:
                self.body = body
                self.com = body.r
                self.mass = body.m
            else:
                self.is_leaf = False
                self.sw = Node(self.quad.sw())
                self.se = Node(self.quad.SE())
                self.nw = Node(self.quad.NW())
                self.ne = Node(self.quad.NE())

                if self.body.in_quad(self.sw.quad):
                    self.sw.insert_body(self.body)
                if self.body.in_quad(self.se.quad):
                    self.se.insert_body(self.body)
                if self.body.in_quad(self.nw.quad):
                    self.nw.insert_body(self.body)
                if self.body.in_quad(self.ne.quad):
                    self.ne.insert_body(self.body)
                self.body = None

                if body.in_quad(self.sw.quad):
                    self.sw.insert_body(body)
                if body.in_quad(self.se.quad):
                    self.se.insert_body(body)
                if body.in_quad(self.nw.quad):
                    self.nw.insert_body(body)
                if body.in_quad(self.ne.quad):
                    self.ne.insert_body(body)

                self.com = (self.mass * self.com + body.m * body.r)/(self.mass + body.m)
                self.mass += body.m
        else:
            assert self.sw is not None
            assert self.se is not None
            assert self.ne is not None
            assert self.nw is not None

            if body.in_quad(self.sw.quad):
                self.sw.insert_body(body)
            if body.in_quad(self.se.quad):
                self.se.insert_body(body)
            if body.in_quad(self.nw.quad):
                self.nw.insert_body(body)
            if body.in_quad(self.ne.quad):
                self.ne.insert_body(body)

    def plot(self):
        if self.body is not None:
            self.body.plot()
        if self.is_leaf:
            self.quad.plot()
        else:
            assert self.sw is not None
            assert self.se is not None
            assert self.ne is not None
            assert self.nw is not None
            self.sw.plot()
            self.se.plot()
            self.nw.plot()
            self.ne.plot()








