# engine/layer.py
import numpy as np

class Layer:
    """
    하나의 이미지 레이어를 나타내는 클래스입니다.
    RGBA 픽셀 배열을 보유하며, 보이기 여부와 이름 속성을 포함합니다.
    """

    def __init__(self, width, height):
        """
        주어진 크기로 레이어를 초기화합니다.

        Args:
            width (int): 레이어의 너비 (픽셀 단위).
            height (int): 레이어의 높이 (픽셀 단위).
        """
        self.pixels = np.zeros((height, width, 4), dtype=np.uint8)
        self.visible = True
        self.name = "Layer"
