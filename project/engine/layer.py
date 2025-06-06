# engine/layer.py

import numpy as np

class Layer:
    def __init__(self, width, height):
        self.pixels = np.zeros((height, width, 4), dtype=np.uint8)
        self.visible = True
        self.name = "Layer"
