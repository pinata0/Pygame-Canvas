# handlers/undo_redo.py
import pygame

def handle_undo_redo(event, keys, undo_stack, redo_stack, vector_layer):
    """
    Ctrl+Z 및 Ctrl+Shift+Z 키 입력에 따라 실행 취소(Undo) 및 다시 실행(Redo)를 처리합니다.

    Undo/Redo 동작은 vector_layer에 Stroke를 추가하거나 제거하거나, 분할을 되돌리는 방식으로 동작합니다.

    Args:
        event (pygame.event.Event): 현재 키보드 이벤트.
        keys (dict): pygame.key.get_pressed() 결과 (사용되지 않음).
        undo_stack (list): 실행 취소 히스토리 스택.
        redo_stack (list): 다시 실행 히스토리 스택.
        vector_layer (VectorLayer): 벡터 레이어 객체.

    Returns:
        tuple: (undo_stack, redo_stack) – 수정된 스택 반환
    """
    if event.type == pygame.KEYDOWN:
        mods = pygame.key.get_mods()

        # Ctrl + Z → Undo
        if event.key == pygame.K_z and mods & pygame.KMOD_CTRL and not mods & pygame.KMOD_SHIFT:
            if undo_stack:
                entry = undo_stack.pop()
                action = entry[0]

                if action == "add_stroke":
                    stroke = entry[1]
                    if stroke in vector_layer.strokes:
                        vector_layer.strokes.remove(stroke)
                        print("↩️ [UNDO] stroke 제거")
                    redo_stack.append(("remove_stroke", stroke))

                elif action == "remove_stroke":
                    stroke = entry[1]
                    vector_layer.add_stroke(stroke)
                    print("↩️ [UNDO] stroke 복원")
                    redo_stack.append(("add_stroke", stroke))

                elif action == "split_stroke":
                    original, parts = entry[1], entry[2]
                    for s in parts:
                        if s in vector_layer.strokes:
                            vector_layer.strokes.remove(s)
                    vector_layer.add_stroke(original)
                    print("↩️ [UNDO] 분할 되돌림")
                    redo_stack.append(("split_stroke", original, parts))

        # Ctrl + Shift + Z → Redo
        elif event.key == pygame.K_z and mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
            if redo_stack:
                entry = redo_stack.pop()
                action = entry[0]

                if action == "remove_stroke":
                    stroke = entry[1]
                    vector_layer.add_stroke(stroke)
                    print("↪️ [REDO] stroke 추가")
                    undo_stack.append(("add_stroke", stroke))

                elif action == "add_stroke":
                    stroke = entry[1]
                    if stroke in vector_layer.strokes:
                        vector_layer.strokes.remove(stroke)
                    print("↪️ [REDO] stroke 제거")
                    undo_stack.append(("remove_stroke", stroke))

                elif action == "split_stroke":
                    original, parts = entry[1], entry[2]
                    if original in vector_layer.strokes:
                        vector_layer.strokes.remove(original)
                    for s in parts:
                        vector_layer.add_stroke(s)
                    print("↪️ [REDO] 분할 재적용")
                    undo_stack.append(("split_stroke", original, parts))

    return undo_stack, redo_stack
