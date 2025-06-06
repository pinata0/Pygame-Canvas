# engine/tools.py
class DrawCommand:
    """
    레이어에 적용된 드로잉 작업을 저장하고 실행/되돌리기 할 수 있는 커맨드 클래스입니다.
    커맨드 패턴을 기반으로 하며, History 객체에서 관리됩니다.
    """

    def __init__(self, layer, prev_state, new_state):
        """
        DrawCommand 객체를 초기화합니다.

        Args:
            layer (Layer): 적용 대상 레이어 객체.
            prev_state (numpy.ndarray): 드로잉 이전 상태의 픽셀 배열 (RGBA).
            new_state (numpy.ndarray): 드로잉 이후 상태의 픽셀 배열 (RGBA).
        """
        self.layer = layer
        self.prev_state = prev_state.copy()
        self.new_state = new_state.copy()

    def execute(self):
        """
        드로잉 작업을 실행합니다.
        레이어의 픽셀을 new_state로 덮어씁니다.
        """
        self.layer.pixels[:] = self.new_state

    def undo(self):
        """
        드로잉 작업을 취소합니다.
        레이어의 픽셀을 prev_state로 되돌립니다.
        """
        self.layer.pixels[:] = self.prev_state
