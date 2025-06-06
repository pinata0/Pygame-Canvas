# utils/helpers.py

import pygame
import datetime
import numpy as np

def save_canvas_as_png(screen, canvas, vector_layer, offset=(0, 0), size=None):
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
    width, height = surface.get_size()
    surface.fill(bg_color)
    for y in range(line_spacing, height, line_spacing):
        for x in range(0, width, 10):
            pygame.draw.line(surface, line_color, (x, y), (x + 5, y), 1)
