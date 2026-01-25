import matplotlib.pyplot as plt
import numpy as np

from quadtree import Quad, QuadTreeNode
from body import Body


tree = QuadTreeNode(Quad(0, 0, 200))
bodies = [Body(np.random.random() * 200, np.random.random() * 200, 10) for i in range(100)]

for body in bodies:
    tree.insert_body(body)
tree.plot(True)
plt.show()
plt.cla()
