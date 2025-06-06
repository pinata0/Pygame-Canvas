# utils/constants.py
import pygame

# ─────────────────────────────
# GUI 레이아웃 설정 상수
# ─────────────────────────────

#: 캔버스 왼쪽 툴바 너비 (px)
TOOLBAR_LEFT = 60

#: 캔버스 상단 툴바 높이 (px)
TOOLBAR_TOP = 20

#: 캔버스 오른쪽 툴바 너비 (px)
TOOLBAR_RIGHT = 40

#: 캔버스 하단 툴바 높이 (px)
TOOLBAR_BOTTOM = 20

# ─────────────────────────────
# 브러시 및 지우개 반지름 제한
# ─────────────────────────────

#: 최소 반지름 (px)
MIN_RADIUS = 1

#: 최대 반지름 (px)
MAX_RADIUS = 100

# ─────────────────────────────
# 캔버스 및 전체 화면 크기
# ─────────────────────────────

#: 그리기 가능한 실제 캔버스 너비 (px)
CANVAS_WIDTH = 512

#: 그리기 가능한 실제 캔버스 높이 (px)
CANVAS_HEIGHT = 512

#: 전체 화면 너비 (툴바 포함)
SCREEN_WIDTH = TOOLBAR_LEFT + CANVAS_WIDTH + TOOLBAR_RIGHT

#: 전체 화면 높이 (툴바 포함)
SCREEN_HEIGHT = TOOLBAR_TOP + CANVAS_HEIGHT + TOOLBAR_BOTTOM

# ─────────────────────────────
# 색상 팔레트: 키보드 단축키 → 색상 매핑
# ─────────────────────────────

#: 키보드 숫자 키 (K_1 ~ K_6) 에 대응하는 RGBA 색상
COLOR_PALETTE = {
    pygame.K_1: (9, 7, 7, 255),         # 검정색?
    pygame.K_2: (229, 58, 64, 255),     # 빨간색
    pygame.K_3: (239, 220, 5, 255),     # 노란색
    pygame.K_4: (48, 169, 222, 255),    # 하늘색
    pygame.K_5: (246, 134, 87, 255),    # 주황색
    pygame.K_6: (144, 85, 162, 255),    # 보라색
}
