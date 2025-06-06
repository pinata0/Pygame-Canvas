# main.py
import pygame
import numpy as np
import datetime

from engine.canvas import Canvas
from engine.stroke import Stroke
from engine.vectorlayer import VectorLayer
from utils.constants import *
from utils.helpers import draw_notebook_background, save_canvas_as_png
from handlers.color_tool import handle_color_change, handle_tool_switch
from handlers.undo_redo import handle_undo_redo
from handlers.mouse_input import handle_mouse_input

def main(is_debug):
    """
    포토샵 클론 애플리케이션의 메인 루프를 실행합니다.

    초기화:
        - pygame 환경 및 화면 설정
        - 캔버스, 벡터 레이어, 커서, 도구 상태 초기화

    이벤트 처리:
        - 키보드 입력: 도구 전환, 색상 변경, Undo/Redo
        - 마우스 입력: 그리기, 지우기, 반경 조절

    렌더링:
        - 캔버스 배경, 벡터 드로잉, 현재 스트로크, 툴바, 커서, 쿼드트리 경계
        - 최종적으로 화면 갱신

    종료:
        - 창 종료 시 pygame.quit() 호출
    """
    # 초기화
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Canvas")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    cursor_img = pygame.image.load("./resources/cursor.png").convert_alpha()
    cursor_rect = cursor_img.get_rect()
    pygame.mouse.set_visible(False)

    canvas = Canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    canvas.add_layer("Base Layer")
    canvas.select_layer(0)

    brush_color = COLOR_PALETTE[pygame.K_3]
    brush_radius = 10
    eraser_radius = 10

    undo_stack, redo_stack = [], []
    current_stroke = None
    current_tool = "brush"
    eraser_mode = "stroke"
    vector_layer = VectorLayer()

    running = True
    while running:
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            brush_color, current_tool, eraser_mode = handle_color_change(event, keys, brush_color, current_tool, eraser_mode)
            current_tool, eraser_mode = handle_tool_switch(event, keys, current_tool, eraser_mode)
            undo_stack, redo_stack = handle_undo_redo(event, keys, undo_stack, redo_stack, vector_layer)
            current_stroke, undo_stack, redo_stack, brush_radius, eraser_radius = handle_mouse_input(
                event, current_tool, eraser_mode, canvas, vector_layer,
                undo_stack, redo_stack, TOOLBAR_LEFT, TOOLBAR_TOP,
                CANVAS_WIDTH, CANVAS_HEIGHT, brush_color, brush_radius,
                eraser_radius, current_stroke
            )

        # 화면 초기화 및 렌더링
        screen.fill((255, 255, 255))

        # 캔버스 픽셀 렌더링
        frame = canvas.render().astype(np.uint8)
        frame = frame[:CANVAS_HEIGHT, :CANVAS_WIDTH]
        image_surface = pygame.surfarray.make_surface(np.transpose(frame[:, :, :3], (1, 0, 2)))
        screen.blit(image_surface, (TOOLBAR_LEFT, TOOLBAR_TOP))

        # 공책 배경 그리기
        draw_notebook_background(screen.subsurface(
            pygame.Rect(TOOLBAR_LEFT, TOOLBAR_TOP, CANVAS_WIDTH, CANVAS_HEIGHT)))

        # 벡터 드로잉 렌더링
        vector_layer.render(screen, offset=(TOOLBAR_LEFT, TOOLBAR_TOP))

        # 현재 그리고 있는 스트로크 실시간 표시
        if current_stroke and current_tool == "brush":
            if len(current_stroke.points) >= 2:
                adjusted_points = [(x + TOOLBAR_LEFT, y + TOOLBAR_TOP) for x, y in current_stroke.points]
                pygame.draw.lines(screen, current_stroke.color[:3], False, adjusted_points, max(1, current_stroke.radius))
            for x, y in current_stroke.points:
                pygame.draw.circle(screen, current_stroke.color[:3], (x + TOOLBAR_LEFT, y + TOOLBAR_TOP), current_stroke.radius // 2)

        # 툴바 및 커서 표시
        from utils.ui import draw_toolbar, draw_cursor_overlay
        draw_toolbar(screen, brush_color, brush_radius, eraser_radius, font, current_tool)
        draw_cursor_overlay(screen, cursor_img, current_tool, brush_radius, eraser_radius)
        
        # 쿼드트리 시각화
        if is_debug:
            if vector_layer.quadtree:
                vector_layer.quadtree.draw(screen, color=(0, 128, 255), thickness=1, offset=(TOOLBAR_LEFT, TOOLBAR_TOP))

        pygame.display.flip()
        clock.tick(180)

    pygame.quit()
