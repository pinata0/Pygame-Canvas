# handlers/color_tool.py

import pygame
from utils.constants import COLOR_PALETTE

def handle_color_change(event, keys, brush_color, current_tool, eraser_mode):
    if event.type == pygame.KEYDOWN and event.key in COLOR_PALETTE:
        brush_color = COLOR_PALETTE[event.key]
        print(f"🎨 Color changed to {brush_color[:3]}")
    return brush_color, current_tool, eraser_mode


def handle_tool_switch(event, keys, current_tool, eraser_mode):
    if event.type == pygame.KEYDOWN:
        if keys[pygame.K_e] and event.key == pygame.K_1:
            current_tool = "eraser"
            eraser_mode = "stroke"
            print("🧹 지우개 모드: 획 지우개 (stroke)")
        elif keys[pygame.K_e] and event.key == pygame.K_2:
            current_tool = "eraser"
            eraser_mode = "area"
            print("🔳 지우개 모드: 영역 지우개 (area)")
        elif event.key == pygame.K_b:
            current_tool = "brush"
            print("🖌️ 브러시 모드로 전환")

    return current_tool, eraser_mode
