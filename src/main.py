import matplotlib.pyplot as plt
from quadtree import Quad, Node
from body import Body
import numpy as np


tree = Node(Quad(0, 0, 200))
bodies = [Body(np.random.random() * 200, np.random.random() * 200, 10) for i in range(100)]

for body in bodies:
    tree.insert_body(body)
tree.plot()
plt.show()
plt.cla()

