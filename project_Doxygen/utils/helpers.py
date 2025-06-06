# utils/helpers.py
import pygame
import datetime
import numpy as np

def save_canvas_as_png(screen, canvas, vector_layer, offset=(0, 0), size=None):
    """
    현재 캔버스와 벡터 레이어를 PNG 이미지로 저장합니다.

    배경은 연두색 줄이 있는 공책 스타일로 렌더링되며,
    픽셀 캔버스와 벡터 드로잉이 함께 결합된 이미지를 생성합니다.

    Args:
        screen (pygame.Surface): 현재 표시 중인 전체 화면 surface (사용되지 않음).
        canvas (Canvas): 픽셀 기반 캔버스 객체.
        vector_layer (VectorLayer): 벡터 레이어 객체.
        offset (tuple): 렌더링 시 오프셋 (x, y). 기본값은 (0, 0).
        size (tuple, optional): 저장할 이미지의 크기 (width, height). 생략 시 캔버스 크기를 사용합니다.
    """
    ox, oy = offset
    width, height = size if size else (canvas.width, canvas.height)
    save_surface = pygame.Surface((width, height))

    frame = canvas.render().astype(np.uint8)
    frame = frame[:height, :width]
    canvas_surface = pygame.surfarray.make_surface(np.transpose(frame[:, :, :3], (1, 0, 2)))
    save_surface.blit(canvas_surface, (0, 0))

    draw_notebook_background(save_surface)
    vector_layer.render(save_surface, offset=(0, 0))

    now = datetime.datetime.now()
    filename = f"saved_{now.strftime('%Y%m%d_%H%M%S')}.png"
    pygame.image.save(save_surface, filename)
    print(f"💾 저장 완료: {filename}")

def draw_notebook_background(surface, line_spacing=40, line_color=(144, 238, 144), bg_color=(255, 255, 255)):
    """
    연두색 줄무늬가 있는 공책 스타일 배경을 그립니다.

    Args:
        surface (pygame.Surface): 배경을 그릴 surface.
        line_spacing (int): 수평 줄 간격 (기본값: 40px).
        line_color (tuple): 줄 색상 (R, G, B). 기본값: 연두색.
        bg_color (tuple): 배경 색상 (R, G, B). 기본값: 흰색.
    """
    width, height = surface.get_size()
    surface.fill(bg_color)
    for y in range(line_spacing, height, line_spacing):
        for x in range(0, width, 10):
            pygame.draw.line(surface, line_color, (x, y), (x + 5, y), 1)
