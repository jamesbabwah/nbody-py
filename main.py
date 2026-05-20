#pylint: disable=missing-module-docstring

import numpy as np
import pygame as pg

from nbody import QuadTreeNode, Body
from nbody.renderer.pgrenderer import PGRenderer



renderer = PGRenderer(600, 600)


tree = QuadTreeNode(0, 0, 600)
bodies = [Body(np.random.random() * 600, np.random.random() * 600, 10) for i in range(1_000)]

for body in bodies:
    tree.insert_body(body)
tree.plot(renderer, True)
renderer.update()

running = True

while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False