"""Benchmark for constructing the tree and adding bodies"""
import numpy as np
import perfplot
import cProfile as cp
import timeit

from nbody.quadtree import Quad, QuadTreeNode
from nbody.body import Body

SIM_RANGE = 1000

def construct_tree(bodies):
    quad = Quad(0, 0, SIM_RANGE)
    tree = QuadTreeNode(quad)
    for body in bodies:
        tree.insert_body(body)


def construct_n_bodies(n):
    bodies = []
    for _ in range(n):
        bodies.append(Body(np.random.random()*SIM_RANGE,np.random.random()*SIM_RANGE, 1))
    return bodies

if __name__ == "__main__":
    bodies = construct_n_bodies(100_000)
    cp.run("construct_tree(bodies)", sort='cumtime')

    
