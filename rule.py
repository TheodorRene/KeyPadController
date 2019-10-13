class Rule:

    def __init__(self, trig_state, new_state, trig_signals, action):
        self.trig_state = trig_state
        self.new_state = new_state
        self.trig_signals = trig_signals
        self.action = action
