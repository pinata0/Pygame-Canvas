import pygame
import sys

# 초기화
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("draw.lines 예제")
clock = pygame.time.Clock()

# 선을 그릴 좌표들
points = [(100, 100), (150, 200), (200, 150), (300, 250), (400, 200)]

# 메인 루프
running = True
while running:
    screen.fill((255, 255, 255))  # 배경 흰색

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 선 그리기
    pygame.draw.lines(
        surface=screen,           # 그릴 대상 surface
        color=(0, 0, 255),        # 선 색상 (파란색)
        closed=False,             # 끝점과 시작점을 연결할지 여부
        points=points,            # 좌표 리스트
        width=3                   # 선의 두께
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
