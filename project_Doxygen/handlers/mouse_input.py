# handlers/mouse_input.py
import pygame
from engine.stroke import Stroke
from utils.constants import MIN_RADIUS, MAX_RADIUS

def handle_mouse_input(
    event,
    current_tool,
    eraser_mode,
    canvas,
    vector_layer,
    undo_stack,
    redo_stack,
    TOOLBAR_LEFT,
    TOOLBAR_TOP,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    brush_color,
    brush_radius,
    eraser_radius,
    current_stroke
):
    """
    마우스 입력 이벤트를 처리합니다.

    클릭, 드래그, 휠 동작에 따라 브러시 그리기, 스트로크/영역 지우기, 반경 조절 등의 작업을 수행합니다.

    Args:
        event (pygame.event.Event): 현재 마우스 이벤트 객체.
        current_tool (str): 현재 선택된 도구 ("brush" 또는 "eraser").
        eraser_mode (str): 지우개 동작 모드 ("stroke" 또는 "area").
        canvas (Canvas): 픽셀 기반 캔버스 객체 (현재는 사용되지 않음).
        vector_layer (VectorLayer): 벡터 기반 레이어 객체.
        undo_stack (list): 실행 취소 스택.
        redo_stack (list): 다시 실행 스택.
        TOOLBAR_LEFT (int): 툴바 왼쪽 여백.
        TOOLBAR_TOP (int): 툴바 상단 여백.
        CANVAS_WIDTH (int): 캔버스 너비.
        CANVAS_HEIGHT (int): 캔버스 높이.
        brush_color (tuple): 브러시 색상 (R, G, B, A).
        brush_radius (int): 브러시 반지름.
        eraser_radius (int): 지우개 반지름.
        current_stroke (Stroke or None): 현재 진행 중인 브러시 Stroke 객체.

    Returns:
        tuple: (current_stroke, undo_stack, redo_stack)
    """
    x, y = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if TOOLBAR_LEFT <= x < TOOLBAR_LEFT + CANVAS_WIDTH and TOOLBAR_TOP <= y < TOOLBAR_TOP + CANVAS_HEIGHT:
            cx, cy = x - TOOLBAR_LEFT, y - TOOLBAR_TOP
            if current_tool == "brush":
                current_stroke = Stroke(brush_color, brush_radius)
                current_stroke.add_point(cx, cy)
            elif current_tool == "eraser":
                if eraser_mode == "stroke":
                    removed = vector_layer.erase_near(cx, cy, eraser_radius)
                    vector_layer.rebuild_quadtree(CANVAS_WIDTH, CANVAS_HEIGHT)
                    if removed:
                        undo_stack.append(("remove_stroke", removed))
                        redo_stack.clear()
                elif eraser_mode == "area":
                    result = vector_layer.partial_erase(x, y, eraser_radius, offset=(TOOLBAR_LEFT, TOOLBAR_TOP))
                    vector_layer.rebuild_quadtree(CANVAS_WIDTH, CANVAS_HEIGHT)
                    if result:
                        original, parts = result
                        undo_stack.append(("split_stroke", original, parts))
                        redo_stack.clear()

    elif event.type == pygame.MOUSEMOTION:
        if pygame.mouse.get_pressed()[0]:
            if TOOLBAR_LEFT <= x < TOOLBAR_LEFT + CANVAS_WIDTH and TOOLBAR_TOP <= y < TOOLBAR_TOP + CANVAS_HEIGHT:
                cx, cy = x - TOOLBAR_LEFT, y - TOOLBAR_TOP

                if current_tool == "brush" and current_stroke:
                    current_stroke.add_point(cx, cy)

                elif current_tool == "eraser":
                    if eraser_mode == "stroke":
                        removed = vector_layer.erase_near(cx, cy, eraser_radius)
                        vector_layer.rebuild_quadtree(CANVAS_WIDTH, CANVAS_HEIGHT)
                        if removed:
                            undo_stack.append(("remove_stroke", removed))
                            redo_stack.clear()

                    elif eraser_mode == "area":
                        result = vector_layer.partial_erase(x, y, eraser_radius, offset=(TOOLBAR_LEFT, TOOLBAR_TOP))
                        vector_layer.rebuild_quadtree(CANVAS_WIDTH, CANVAS_HEIGHT)
                        if result:
                            original, parts = result
                            undo_stack.append(("split_stroke", original, parts))
                            redo_stack.clear()

    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        if current_tool == "brush" and current_stroke:
            vector_layer.add_stroke(current_stroke)
            vector_layer.rebuild_quadtree(CANVAS_WIDTH, CANVAS_HEIGHT)
            undo_stack.append(("add_stroke", current_stroke))
            redo_stack.clear()
            current_stroke = None

    if event.type == pygame.MOUSEWHEEL:
        if current_tool == "brush":
            brush_radius += event.y
            brush_radius = max(MIN_RADIUS, min(MAX_RADIUS, brush_radius))
        elif current_tool == "eraser":
            eraser_radius += event.y
            eraser_radius = max(MIN_RADIUS, min(MAX_RADIUS, eraser_radius))

    return current_stroke, undo_stack, redo_stack, brush_radius, eraser_radius
