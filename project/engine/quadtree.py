# engine/quadtree.py

import pygame

class QuadtreeNode:
    def __init__(self, x, y, width, height, capacity=4):
        self.boundary = pygame.Rect(x, y, width, height)
        self.capacity = capacity
        self.points = []  # (stroke_idx, point_idx, x, y)
        self.divided = False

    def insert(self, stroke_idx, point_idx, x, y):
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
        x, y, w, h = self.boundary
        hw, hh = w // 2, h // 2
        self.nw = QuadtreeNode(x, y, hw, hh)
        self.ne = QuadtreeNode(x + hw, y, hw, hh)
        self.sw = QuadtreeNode(x, y + hh, hw, hh)
        self.se = QuadtreeNode(x + hw, y + hh, hw, hh)
        self.divided = True

    def query_circle(self, cx, cy, radius):
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
        x, y, w, h = self.boundary
        closest_x = max(x, min(cx, x + w))
        closest_y = max(y, min(cy, y + h))
        dx, dy = closest_x - cx, closest_y - cy
        return dx * dx + dy * dy <= r * r

    def draw(self, surface, color=(100, 200, 255), thickness=1, offset=(0, 0)):
        ox, oy = offset
        rect = pygame.Rect(self.boundary.x + ox, self.boundary.y + oy,
                           self.boundary.width, self.boundary.height)
        pygame.draw.rect(surface, color, rect, thickness)
        if self.divided:
            self.nw.draw(surface, color, thickness, offset)
            self.ne.draw(surface, color, thickness, offset)
            self.sw.draw(surface, color, thickness, offset)
            self.se.draw(surface, color, thickness, offset)
