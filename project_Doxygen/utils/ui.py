# utils/ui.py
import pygame
from utils.constants import *

def draw_toolbar(screen, brush_color, brush_radius, eraser_radius, font, current_tool):
    """
    툴바 영역을 그립니다.

    - 화면 상/하/좌/우의 툴바 배경을 칠하고
    - 현재 색상 미리보기 박스를 표시하며
    - 현재 도구와 반지름 정보를 텍스트로 출력합니다.

    Args:
        screen (pygame.Surface): 렌더링할 대상 화면 surface.
        brush_color (tuple): 현재 브러시 색상 (R, G, B, A).
        brush_radius (int): 브러시 반지름 (px).
        eraser_radius (int): 지우개 반지름 (px).
        font (pygame.font.Font): 텍스트 출력에 사용할 폰트 객체.
        current_tool (str): 현재 도구 ("brush" 또는 "eraser").
    """
    TOOLBAR_BG_COLOR = (157, 200, 200)
    screen.fill(TOOLBAR_BG_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, TOOLBAR_TOP))
    screen.fill(TOOLBAR_BG_COLOR, pygame.Rect(0, SCREEN_HEIGHT - TOOLBAR_BOTTOM, SCREEN_WIDTH, TOOLBAR_BOTTOM))
    screen.fill(TOOLBAR_BG_COLOR, pygame.Rect(0, 0, TOOLBAR_LEFT, SCREEN_HEIGHT))
    screen.fill(TOOLBAR_BG_COLOR, pygame.Rect(SCREEN_WIDTH - TOOLBAR_RIGHT, 0, TOOLBAR_RIGHT, SCREEN_HEIGHT))

    coordinate = (TOOLBAR_LEFT + CANVAS_WIDTH + TOOLBAR_RIGHT // 2, TOOLBAR_TOP + TOOLBAR_RIGHT // 2)
    margin = TOOLBAR_RIGHT // (3/2)
    coordinate_range = (coordinate[0] - margin//2 , coordinate[1] - margin//2, margin, margin)
    pygame.draw.rect(screen, brush_color[:3], coordinate_range)
    pygame.draw.rect(screen, (255, 255, 255), coordinate_range, 2)

    text = f"Brush: {brush_radius}px" if current_tool == "brush" else f"Eraser: {eraser_radius}px"
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (TOOLBAR_LEFT, TOOLBAR_TOP + CANVAS_HEIGHT))

def draw_cursor_overlay(screen, cursor_img, current_tool, brush_radius, eraser_radius):
    """
    마우스 커서 주변에 도구 반경을 시각적으로 표시합니다.

    - 커서 이미지 표시
    - 브러시 또는 지우개 반경을 원 형태로 렌더링

    Args:
        screen (pygame.Surface): 그릴 대상 화면 surface.
        cursor_img (pygame.Surface): 표시할 커서 이미지.
        current_tool (str): 현재 선택된 도구 ("brush" 또는 "eraser").
        brush_radius (int): 브러시 반지름 (px).
        eraser_radius (int): 지우개 반지름 (px).
    """
    mouse_pos = pygame.mouse.get_pos()
    cursor_rect = cursor_img.get_rect(center=mouse_pos)
    screen.blit(cursor_img, cursor_rect)

    radius = int(brush_radius // 1.5) if current_tool == "brush" else eraser_radius
    pygame.draw.circle(screen, (0, 0, 0), mouse_pos, radius, 1)
