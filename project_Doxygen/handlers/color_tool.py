# handlers/color_tool.py
import pygame
from utils.constants import COLOR_PALETTE

def handle_color_change(event, keys, brush_color, current_tool, eraser_mode):
    """
    색상 변경 이벤트를 처리합니다.

    숫자 키(1~9)를 눌렀을 때 COLOR_PALETTE에서 대응되는 색상을 선택합니다.

    Args:
        event (pygame.event.Event): 현재 키보드 이벤트.
        keys (dict): pygame.key.get_pressed() 결과.
        brush_color (tuple): 현재 브러시 색상.
        current_tool (str): 현재 선택된 도구 ("brush" 또는 "eraser").
        eraser_mode (str): 현재 지우개 모드 ("stroke" 또는 "area").

    Returns:
        tuple: (변경된 brush_color, current_tool, eraser_mode)
    """
    if event.type == pygame.KEYDOWN and event.key in COLOR_PALETTE:
        brush_color = COLOR_PALETTE[event.key]
        print(f"🎨 Color changed to {brush_color[:3]}")
    return brush_color, current_tool, eraser_mode


def handle_tool_switch(event, keys, current_tool, eraser_mode):
    """
    도구 전환 이벤트를 처리합니다.

    - E+1: 획 지우개(stroke eraser) 모드로 전환  
    - E+2: 영역 지우개(area eraser) 모드로 전환  
    - B: 브러시 모드로 전환

    Args:
        event (pygame.event.Event): 현재 키보드 이벤트.
        keys (dict): pygame.key.get_pressed() 결과.
        current_tool (str): 현재 선택된 도구 ("brush" 또는 "eraser").
        eraser_mode (str): 현재 지우개 모드 ("stroke" 또는 "area").

    Returns:
        tuple: (변경된 current_tool, eraser_mode)
    """
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
