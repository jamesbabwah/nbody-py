import numpy as np
import matplotlib.pyplot as plt


class Body:
    def __init__(self, rx, ry, m, vx = 0.0, vy = 0.0) -> None:
        self.r = np.array([rx, ry])
        self.v = np.array([vx, vy])
        self.m = m
        self.F = np.array([0.0, 0.0])

    def in_quad(self, quad):
        return ((quad.r[0] < self.r[0] and quad.r[0] + quad.length > self.r[0]) and
            (quad.r[1] < self.r[1] and quad.r[1] + quad.length > self.r[1]))


    def plot(self):
        plt.scatter(self.r[0], self.r[1], 4.0, 'black')