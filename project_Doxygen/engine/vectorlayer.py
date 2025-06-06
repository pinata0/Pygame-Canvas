# engine/vectorlayer.py
import pygame
from engine.stroke import Stroke
from engine.quadtree import QuadtreeNode

class VectorLayer:
    """
    벡터 기반 드로잉을 위한 레이어 클래스입니다.

    Stroke 객체들을 리스트로 관리하며, Quadtree를 통해 영역 기반 탐색 및 지우기 기능을 지원합니다.
    """

    def __init__(self):
        """
        VectorLayer 객체를 초기화합니다.
        """
        self.strokes = []
        self.quadtree = None

    def add_stroke(self, stroke):
        """
        새로운 스트로크를 추가하고, 쿼드트리에 좌표를 등록합니다.

        Args:
            stroke (Stroke): 추가할 스트로크 객체.
        """
        self.strokes.append(stroke)
        if self.quadtree:
            for p_idx, (x, y) in enumerate(stroke.points):
                self.quadtree.insert(len(self.strokes) - 1, p_idx, x, y)

    def render(self, surface, offset=(0, 0)):
        """
        모든 스트로크를 화면에 렌더링합니다.

        Args:
            surface (pygame.Surface): 그릴 대상 surface 객체.
            offset (tuple): (x, y) 오프셋 좌표.
        """
        ox, oy = offset
        for stroke in self.strokes:
            if len(stroke.points) >= 2:
                adjusted = [(x + ox, y + oy) for x, y in stroke.points]
                pygame.draw.lines(surface, stroke.color[:3], False, adjusted, max(1, stroke.radius))
            for x, y in stroke.points:
                pygame.draw.circle(surface, stroke.color[:3], (x + ox, y + oy), stroke.radius // 2)

    def rebuild_quadtree(self, width, height):
        """
        현재 보유한 스트로크들을 기준으로 쿼드트리를 재구성합니다.

        Args:
            width (int): 쿼드트리 전체 영역 너비.
            height (int): 쿼드트리 전체 영역 높이.
        """
        self.quadtree = QuadtreeNode(0, 0, width, height)
        for s_idx, stroke in enumerate(self.strokes):
            for p_idx, (x, y) in enumerate(stroke.points):
                self.quadtree.insert(s_idx, p_idx, x, y)

    def erase_near(self, x, y, radius, offset=(0, 0)):
        """
        반지름 내에 있는 전체 스트로크를 통째로 제거합니다.

        Args:
            x (int): 마우스 X 좌표.
            y (int): 마우스 Y 좌표.
            radius (float): 반경.
            offset (tuple): 화면 렌더링 기준 오프셋.

        Returns:
            Stroke or None: 삭제된 스트로크 하나를 반환하거나, 없으면 None.
        """
        ox, oy = offset
        cx, cy = x - ox, y - oy
        if not self.quadtree:
            return None
        near_points = self.quadtree.query_circle(cx, cy, radius)
        stroke_indices = set(s_idx for s_idx, *_ in near_points)
        erased = []
        for s_idx in sorted(stroke_indices, reverse=True):
            if 0 <= s_idx < len(self.strokes):
                erased.append(self.strokes.pop(s_idx))
        return erased[0] if erased else None

    def partial_erase(self, x, y, radius, offset=(0, 0)):
        """
        반지름 내에 있는 점들만 제거하고 스트로크를 분할합니다.

        Args:
            x (int): 마우스 X 좌표.
            y (int): 마우스 Y 좌표.
            radius (float): 반경.
            offset (tuple): 화면 오프셋.

        Returns:
            tuple or None: (원래 스트로크, 분할된 스트로크 리스트) 또는 None.
        """
        ox, oy = offset
        cx, cy = x - ox, y - oy
        if not self.quadtree:
            return None
        near_points = self.quadtree.query_circle(cx, cy, radius)
        affected = {}
        for s_idx, p_idx, *_ in near_points:
            affected.setdefault(s_idx, []).append(p_idx)
        for s_idx in sorted(affected.keys(), reverse=True):
            if 0 <= s_idx < len(self.strokes):
                stroke = self.strokes.pop(s_idx)
                indices = sorted(affected[s_idx])
                parts = self.split_stroke(stroke, indices)
                for s in parts:
                    self.strokes.append(s)
                    if self.quadtree:
                        new_s_idx = len(self.strokes) - 1
                        for p_idx, (x, y) in enumerate(s.points):
                            self.quadtree.insert(new_s_idx, p_idx, x, y)
                return stroke, parts
        return None

    @staticmethod
    def split_stroke(stroke, erased_indices):
        """
        지정된 인덱스를 기준으로 스트로크를 여러 부분으로 나눕니다.

        Args:
            stroke (Stroke): 분할할 원본 스트로크.
            erased_indices (list): 삭제할 점들의 인덱스 리스트.

        Returns:
            list[Stroke]: 분할된 Stroke 객체들의 리스트.
        """
        if not erased_indices:
            return [stroke]
        segments, current = [], []
        erased_set = set(erased_indices)
        for i, pt in enumerate(stroke.points):
            if i in erased_set:
                if current:
                    s = Stroke(stroke.color, stroke.radius)
                    s.points = current
                    segments.append(s)
                    current = []
            else:
                current.append(pt)
        if current:
            s = Stroke(stroke.color, stroke.radius)
            s.points = current
            segments.append(s)
        return segments
