# handlers/undo_redo.py

import pygame

def handle_undo_redo(event, keys, undo_stack, redo_stack, vector_layer):
    if event.type == pygame.KEYDOWN:
        mods = pygame.key.get_mods()

        if event.key == pygame.K_z and mods & pygame.KMOD_CTRL and not mods & pygame.KMOD_SHIFT:
            # Ctrl+Z: Undo
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

        elif event.key == pygame.K_z and mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
            # Ctrl+Shift+Z: Redo
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
