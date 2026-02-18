#pylint: disable=missing-module-docstring

import numpy as np

from nbody import Quad, QuadTreeNode, BodyAttributes
from nbody.renderer.pgrenderer import PGRenderer


renderer = PGRenderer(600, 600)


tree = QuadTreeNode(Quad(0, 0, 600))
bodies = [BodyAttributes(np.random.random() * 600, np.random.random() * 600, 10) for i in range(100)]

for body in bodies:
    tree.insert_body(body)
tree.plot(renderer, True)
renderer.update()

input()
