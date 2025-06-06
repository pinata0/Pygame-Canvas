# engine/stroke.py
class Stroke:
    """
    하나의 브러시 스트로크를 표현하는 클래스입니다.
    색상, 반지름, 좌표 점들의 리스트를 보유합니다.
    """

    def __init__(self, color, radius):
        """
        Stroke 객체를 초기화합니다.

        Args:
            color (tuple): (R, G, B, A) 형태의 색상 튜플.
            radius (int): 브러시의 반지름 (굵기).
        """
        self.color = color
        self.radius = radius
        self.points = []

    def add_point(self, x, y):
        """
        새로운 점을 스트로크에 추가합니다.  
        일정 거리 이상일 경우, 중간 점을 보간하여 부드러운 선을 생성합니다.

        Args:
            x (int): 추가할 점의 X 좌표.
            y (int): 추가할 점의 Y 좌표.
        """
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

        # 일정 거리 이상일 경우 보간 수행
        SPEED_THRESHOLD = 3  # 픽셀 단위

        if dist > SPEED_THRESHOLD:
            # 보간 간격은 반지름에 비례하여 설정
            spacing = max(1.0, self.radius * 0.15)
            steps = int(dist // spacing)
            for i in range(1, steps + 1):
                t = i / steps
                interp_x = int(x0 + t * dx)
                interp_y = int(y0 + t * dy)
                self.points.append((interp_x, interp_y))
        else:
            self.points.append(new_point)
