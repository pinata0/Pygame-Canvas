# engine/history.py
from collections import deque

class History:
    """
    실행 취소(Undo) 및 다시 실행(Redo)을 지원하는 히스토리 관리 클래스입니다.
    커맨드 패턴 기반으로 동작하며, 최대 크기를 가진 스택으로 구성됩니다.
    """

    def __init__(self, max_size=50):
        """
        History 객체를 초기화합니다.

        Args:
            max_size (int): 저장 가능한 최대 명령 수입니다. 기본값은 50입니다.
        """
        self.undo_stack = deque(maxlen=max_size)
        self.redo_stack = deque(maxlen=max_size)

    def execute(self, command):
        """
        새로운 명령을 실행하고 Undo 스택에 저장합니다.
        Redo 스택은 초기화됩니다.

        Args:
            command: `execute()`와 `undo()` 메서드를 포함하는 커맨드 객체입니다.
        """
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self):
        """
        가장 최근 명령을 실행 취소하고, Redo 스택에 추가합니다.
        """
        if self.undo_stack:
            cmd = self.undo_stack.pop()
            cmd.undo()
            self.redo_stack.append(cmd)

    def redo(self):
        """
        가장 최근 취소된 명령을 다시 실행하고, Undo 스택에 추가합니다.
        """
        if self.redo_stack:
            cmd = self.redo_stack.pop()
            cmd.execute()
            self.undo_stack.append(cmd)
