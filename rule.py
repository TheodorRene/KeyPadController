class Rule:

    def __init__(self, trig_state, new_state, trig_signal, action):
        self.trig_state = trig_state
        self.new_state = new_state
        self.trig_signal = trig_signal
        self.action = action
