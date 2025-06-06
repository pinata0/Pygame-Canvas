# engine/canvas.py
import numpy as np
from .layer import Layer

class Canvas:
    """
    여러 개의 레이어를 관리하며 그리기 및 렌더링을 지원하는 캔버스 클래스입니다.
    """

    def __init__(self, width, height):
        """
        캔버스를 초기화합니다.

        Args:
            width (int): 캔버스의 너비 (픽셀 단위).
            height (int): 캔버스의 높이 (픽셀 단위).
        """
        self.width = width
        self.height = height
        self.layers = []
        self.active_layer_index = None

    def add_layer(self, name=None):
        """
        새로운 레이어를 추가합니다.

        Args:
            name (str, optional): 레이어 이름입니다. 지정하지 않으면 기본 이름이 자동 생성됩니다.
        """
        layer = Layer(self.width, self.height)
        layer.name = name or f"Layer {len(self.layers)}"
        self.layers.append(layer)
        self.active_layer_index = len(self.layers) - 1

    def delete_layer(self, index):
        """
        지정한 인덱스의 레이어를 삭제합니다.

        Args:
            index (int): 삭제할 레이어의 인덱스입니다.
        """
        if 0 <= index < len(self.layers):
            removed = self.layers.pop(index)
            if not self.layers:
                self.active_layer_index = None
            else:
                self.active_layer_index = min(index, len(self.layers) - 1)

    def select_layer(self, index):
        """
        현재 활성화할 레이어를 선택합니다.

        Args:
            index (int): 선택할 레이어의 인덱스입니다.
        """
        if 0 <= index < len(self.layers):
            self.active_layer_index = index

    def get_active_layer(self):
        """
        현재 활성화된 레이어를 반환합니다.

        Returns:
            Layer: 활성 레이어 객체입니다. 없으면 None을 반환합니다.
        """
        if self.active_layer_index is None:
            return None
        return self.layers[self.active_layer_index]

    def draw_circle(self, x, y, radius, color):
        """
        현재 활성 레이어에 원형 브러시로 색상을 칠합니다.

        Args:
            x (int): 원의 중심 X 좌표.
            y (int): 원의 중심 Y 좌표.
            radius (int): 원의 반지름.
            color (tuple): (R, G, B, A) 형태의 색상 튜플입니다.
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
        """
        모든 보이는 레이어를 합성하여 최종 이미지를 생성합니다.

        Returns:
            numpy.ndarray: 합성된 최종 RGBA 이미지입니다.
        """
        result = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        for layer in self.layers:
            if layer.visible:
                result = self.alpha_blend(result, layer.pixels)
        return result

    def alpha_blend(self, base, overlay):
        """
        두 이미지(RGBA)를 알파 블렌딩합니다.

        Args:
            base (numpy.ndarray): 배경 이미지.
            overlay (numpy.ndarray): 덮어씌울 이미지.

        Returns:
            numpy.ndarray: 블렌딩된 이미지입니다.
        """
        alpha = overlay[:, :, 3:] / 255.0
        return (1 - alpha) * base + alpha * overlay
