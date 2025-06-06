# engine/vectorlayer.py

import pygame
from engine.stroke import Stroke
from engine.quadtree import QuadtreeNode

class VectorLayer:
    def __init__(self):
        self.strokes = []
        self.quadtree = None

    def add_stroke(self, stroke):
        self.strokes.append(stroke)
        if self.quadtree:
            for p_idx, (x, y) in enumerate(stroke.points):
                self.quadtree.insert(len(self.strokes) - 1, p_idx, x, y)

    def render(self, surface, offset=(0, 0)):
        ox, oy = offset
        for stroke in self.strokes:
            if len(stroke.points) >= 2:
                adjusted = [(x + ox, y + oy) for x, y in stroke.points]
                pygame.draw.lines(surface, stroke.color[:3], False, adjusted, max(1, stroke.radius))
            for x, y in stroke.points:
                pygame.draw.circle(surface, stroke.color[:3], (x + ox, y + oy), stroke.radius // 2)

    def rebuild_quadtree(self, width, height):
        self.quadtree = QuadtreeNode(0, 0, width, height)
        for s_idx, stroke in enumerate(self.strokes):
            for p_idx, (x, y) in enumerate(stroke.points):
                self.quadtree.insert(s_idx, p_idx, x, y)

    def erase_near(self, x, y, radius, offset=(0, 0)):
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
