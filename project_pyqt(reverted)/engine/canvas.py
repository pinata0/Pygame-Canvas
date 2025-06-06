import numpy as np
from .layer import Layer

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layers = []
        self.active_layer_index = None

    def add_layer(self, name=None):
        layer = Layer(self.width, self.height)
        layer.name = name or f"Layer {len(self.layers)}"
        self.layers.append(layer)
        self.active_layer_index = len(self.layers) - 1

    def delete_layer(self, index):
        if 0 <= index < len(self.layers):
            removed = self.layers.pop(index)
            if not self.layers:
                self.active_layer_index = None
            else:
                self.active_layer_index = min(index, len(self.layers) - 1)

    def select_layer(self, index):
        if 0 <= index < len(self.layers):
            self.active_layer_index = index

    def get_active_layer(self):
        if self.active_layer_index is None:
            return None
        return self.layers[self.active_layer_index]

    def draw_circle(self, x, y, radius, color):
        """
        현재 선택된 레이어에 원형 브러시로 그리기
        - x, y: 중심 좌표
        - radius: 반지름
        - color: (R, G, B, A)
        """
        layer = self.get_active_layer()
        if layer is None:
            print("❌ No active layer selected.")
            return

        yy, xx = np.ogrid[:self.height, :self.width]
        mask = (xx - x)**2 + (yy - y)**2 <= radius**2
        layer.pixels[mask] = color
        print(f"🖌️ Drew circle on layer '{layer.name}' at ({x}, {y})")

    def render(self):
        result = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        for layer in self.layers:
            if layer.visible:
                result = self.alpha_blend(result, layer.pixels)
        return result

    def alpha_blend(self, base, overlay):
        alpha = overlay[:, :, 3:] / 255.0
        return (1 - alpha) * base + alpha * overlay
