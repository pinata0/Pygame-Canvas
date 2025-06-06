# utils/ui.py

import pygame
from utils.constants import *

def draw_toolbar(screen, brush_color, brush_radius, eraser_radius, font, current_tool):
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
    mouse_pos = pygame.mouse.get_pos()
    cursor_rect = cursor_img.get_rect(center=mouse_pos)
    screen.blit(cursor_img, cursor_rect)

    radius = int(brush_radius // 1.5) if current_tool == "brush" else eraser_radius
    pygame.draw.circle(screen, (0, 0, 0), mouse_pos, radius, 1)
