class DrawCommand:
    def __init__(self, layer, prev_state, new_state):
        self.layer = layer
        self.prev_state = prev_state.copy()
        self.new_state = new_state.copy()

    def execute(self):
        self.layer.pixels[:] = self.new_state

    def undo(self):
        self.layer.pixels[:] = self.prev_state
