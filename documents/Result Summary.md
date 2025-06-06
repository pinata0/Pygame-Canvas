Painter: 포토샵 클론코딩 프로젝트 문서

1. 프로젝트 개요
프로젝트 명: Painter

개발 목적: Python 기반의 포토샵 클론 구현

사용 기술: Python, Pygame, NumPy, (추후 PyQt로 확장 예정)

주요 기능: 벡터 드로잉, 브러시/지우개 도구, 레이어 시스템, Undo/Redo, PNG 저장

2. 기술 스택
GUI: Pygame (→ PyQt로 리팩토링 예정)

그래픽 처리: NumPy (픽셀 조작), Pygame.draw (벡터/도형 렌더링)

자료구조: VectorLayer, Stroke, Quadtree 등 커스텀 구조 사용

기타 도구: Quadtree로 빠른 충돌 탐지 및 지우개 최적화

3. 주요 모듈 구성
main.py: 이벤트 루프, 툴 선택, 화면 렌더링

engine/canvas.py: 캔버스 관리 (픽셀 기반 또는 벡터 기반)

engine/vectorlayer.py: 드로잉 객체 관리, Quadtree 통합

engine/stroke.py: 단일 스트로크 객체 정의

engine/quadtree.py: 쿼드트리 자료구조 구현

handlers/: 입력 이벤트에 따른 툴 전환 및 처리 함수들

gui/: (예정) PyQt 기반 GUI 컴포넌트들

4. 핵심 기능 설명
브러시 도구:

마우스 드래그를 통해 점을 연결한 선 그리기

Stroke 객체에 연속된 좌표 추가

지우개 도구:

Stroke Erase: 일정 반경 내 모든 stroke 삭제

Area Erase: stroke의 일부분만 제거하고 나눔

Quadtree 기반으로 삭제 대상 점을 빠르게 탐지

삭제 후 좌우로 stroke 분할

Undo/Redo 시스템:

스택 기반 이력 저장 및 되돌리기 기능 구현

레이어 시스템:

여러 VectorLayer를 쌓아 복수 레이어 지원 (기본 1개 구현됨)

파일 저장 기능:

현재 화면을 .png 형식으로 저장

5. 사용자 인터페이스

화면 밑 : 선택된 도구, 크기 표시

화면 오른쪽 : 선택된 색상 표시 박스

마우스 포인터 : 마우스 포인터 모양 변경, 도구 크기 영역 표시

마우스 휠 : 브러쉬/지우개 크기 조절

키보드 단축키:

B: 브러시

E+1: 획 지우개

E+2 : 영역 지우개

1~9: 색상 선택

Z: Undo, Y: Redo

S: 이미지 저장

6. 기술적 특징 및 최적화
지우개 기능은 Quadtree를 활용해 수천 개의 점 중 빠른 탐색 가능

브러시는 실시간 마우스 좌표 추적으로 동작, 렌더링 최적화 포함

툴 전환은 handler를 분리해 가독성과 유지보수성을 확보

7. 리팩토링 및 확장 계획
PyQt5 기반 GUI로 전환

도킹 UI, 색상 선택기, 멀티 창 지원 예정

Layer 별 숨김/잠금 기능 추가

히스토리 시각화 및 타임라인 기능 실험 예정