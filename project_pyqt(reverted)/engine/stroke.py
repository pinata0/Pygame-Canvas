class Stroke:
    def __init__(self, color, radius):
        self.color = color
        self.radius = radius
        self.points = []

    def add_point(self, x, y):
        new_point = (x, y)
        if not self.points:
            self.points.append(new_point)
            return

        last_point = self.points[-1]
        x0, y0 = last_point
        x1, y1 = new_point

        dx = x1 - x0
        dy = y1 - y0
        dist = (dx ** 2 + dy ** 2) ** 0.5

        # ✅ 일정 거리 이상만 보간 수행
        SPEED_THRESHOLD = 3  # 이 거리 이상이면 보간

        if dist > SPEED_THRESHOLD:
            # 보간 간격을 브러시 반지름에 비례하여 결정
            spacing = max(1.0, self.radius * 0.15)
            steps = int(dist // spacing)
            for i in range(1, steps + 1):
                t = i / steps
                interp_x = int(x0 + t * dx)
                interp_y = int(y0 + t * dy)
                self.points.append((interp_x, interp_y))
        else:
            self.points.append(new_point)
