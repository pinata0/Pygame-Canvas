# engine/quadtree.py
import pygame

class QuadtreeNode:
    """
    2D 공간을 사분할하여 점 데이터를 효율적으로 저장하고 검색할 수 있는 Quadtree 노드 클래스입니다.

    각 노드는 일정 개수(capacity)까지 점을 저장하며, 그 이상이 되면 4개의 자식 노드로 분할(subdivide)됩니다.
    """

    def __init__(self, x, y, width, height, capacity=4):
        """
        쿼드트리 노드를 초기화합니다.

        Args:
            x (int): 사각형 왼쪽 상단 x 좌표.
            y (int): 사각형 왼쪽 상단 y 좌표.
            width (int): 사각형 너비.
            height (int): 사각형 높이.
            capacity (int): 분할 전까지 저장할 수 있는 최대 점 개수. 기본값은 4.
        """
        self.boundary = pygame.Rect(x, y, width, height)
        self.capacity = capacity
        self.points = []  # (stroke_idx, point_idx, x, y)
        self.divided = False

    def insert(self, stroke_idx, point_idx, x, y):
        """
        쿼드트리에 점을 삽입합니다.

        Args:
            stroke_idx (int): 해당 점이 속한 스트로크의 인덱스.
            point_idx (int): 스트로크 내에서의 점 인덱스.
            x (float): 점의 x 좌표.
            y (float): 점의 y 좌표.

        Returns:
            bool: 삽입 성공 여부.
        """
        if not self.boundary.collidepoint(x, y):
            return False
        if len(self.points) < self.capacity:
            self.points.append((stroke_idx, point_idx, x, y))
            return True
        if not self.divided:
            self.subdivide()
        return (
            self.nw.insert(stroke_idx, point_idx, x, y) or
            self.ne.insert(stroke_idx, point_idx, x, y) or
            self.sw.insert(stroke_idx, point_idx, x, y) or
            self.se.insert(stroke_idx, point_idx, x, y)
        )

    def subdivide(self):
        """
        현재 노드를 4개의 자식 노드로 분할합니다.
        """
        x, y, w, h = self.boundary
        hw, hh = w // 2, h // 2
        self.nw = QuadtreeNode(x, y, hw, hh)
        self.ne = QuadtreeNode(x + hw, y, hw, hh)
        self.sw = QuadtreeNode(x, y + hh, hw, hh)
        self.se = QuadtreeNode(x + hw, y + hh, hw, hh)
        self.divided = True

    def query_circle(self, cx, cy, radius):
        """
        원형 영역과 겹치는 점들을 쿼리합니다.

        Args:
            cx (float): 원의 중심 x 좌표.
            cy (float): 원의 중심 y 좌표.
            radius (float): 원의 반지름.

        Returns:
            list[tuple]: (stroke_idx, point_idx, x, y) 형식의 점 리스트.
        """
        found = []
        if not self._intersects_circle(cx, cy, radius):
            return found
        for s_idx, p_idx, px, py in self.points:
            if (px - cx)**2 + (py - cy)**2 <= radius**2:
                found.append((s_idx, p_idx, px, py))
        if self.divided:
            found += self.nw.query_circle(cx, cy, radius)
            found += self.ne.query_circle(cx, cy, radius)
            found += self.sw.query_circle(cx, cy, radius)
            found += self.se.query_circle(cx, cy, radius)
        return found

    def _intersects_circle(self, cx, cy, r):
        """
        현재 사각형이 주어진 원과 겹치는지 여부를 판별합니다.

        Args:
            cx (float): 원 중심의 x 좌표.
            cy (float): 원 중심의 y 좌표.
            r (float): 원의 반지름.

        Returns:
            bool: 겹치면 True, 아니면 False.
        """
        x, y, w, h = self.boundary
        closest_x = max(x, min(cx, x + w))
        closest_y = max(y, min(cy, y + h))
        dx, dy = closest_x - cx, closest_y - cy
        return dx * dx + dy * dy <= r * r

    def draw(self, surface, color=(100, 200, 255), thickness=1, offset=(0, 0)):
        """
        현재 노드의 사각 영역을 시각화합니다.

        Args:
            surface (pygame.Surface): 그릴 대상 surface.
            color (tuple): 사각형의 색상 (R, G, B).
            thickness (int): 테두리 선의 두께.
            offset (tuple): (x, y) 오프셋 좌표.
        """
        ox, oy = offset
        rect = pygame.Rect(self.boundary.x + ox, self.boundary.y + oy,
                           self.boundary.width, self.boundary.height)
        pygame.draw.rect(surface, color, rect, thickness)
        if self.divided:
            self.nw.draw(surface, color, thickness, offset)
            self.ne.draw(surface, color, thickness, offset)
            self.sw.draw(surface, color, thickness, offset)
            self.se.draw(surface, color, thickness, offset)
