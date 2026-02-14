#pylint: disable=C0114

import numpy as np

from quadtree import Quad, QuadTreeNode
from body import Body
from renderer.pgrenderer import PGRenderer


renderer = PGRenderer(600, 600)


tree = QuadTreeNode(Quad(0, 0, 600))
bodies = [Body(np.random.random() * 600, np.random.random() * 600, 10) for i in range(100)]

for body in bodies:
    tree.insert_body(body)
tree.plot(renderer)
renderer.update()
