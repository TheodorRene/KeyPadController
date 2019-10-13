from enum  import Enum
from rule import Rule

class State(Enum):
    S0 = "inital state"
    S1 = "reading input"
    S2 = "verifying"
    S3 = "logged in"
    s4 = "first password change"
    s5 = "second password change"

class FSM:
    def __init__(self, agent):
        self.state = State.S0
        self.rules = []
        self.gen_rules()
        self.agent = agent
        self.debug = True

    def add_rule(self, rule):
        self.rules.append(rule)

    def run_rules(self, signal):
        if self.debug:
            print("Current state: ", self.state)
        for rule in self.rules:
            if self.apply_rule(rule, signal):
                self.fire_rule(rule, signal)
                return
        print("Invalid char")
        self.change_state(State.S0)

    def apply_rule(self, rule, signal):
        if self.state == rule.trig_state and signal in rule.trig_signals:
            return True
        return False
    def change_state(self, new_state):
        print("Changing state", self.state, " ->" , new_state)
        self.state = new_state

    def fire_rule(self, rule, signal):
        rule.action(self.agent, signal)
        self.change_state(rule.new_state)
        print("New state: ", self.state)



    def gen_rules(self):
        # Inital state -> Reading
        R1 = Rule(State.S0, State.S1, [str(i) for i in range(10)], lambda agent, signal: agent.append_buffer(signal))
        # Reading -> Reading
        R1_1 = Rule(State.S1, State.S1, [str(i) for i in range(10)], lambda agent, signal: agent.append_buffer(signal))
        # Reading -> Verify
        R2 = Rule(State.S1, State.S2,['*'], lambda agent, signal: agent.set_override_signal(signal))
        # Verify -> Init State
        R3 = Rule(State.S2, State.S0, [False], lambda agent, signal: agent.reset_buffer(signal))
        # Verify -> logged in
        R4 = Rule(State.S2, State.S3, [True], lambda agent,signal: agent.update_status(signal))
        R5 = Rule(State.S3, State.S4, ['*'], lambda agent,signal: agent.reset_buffer(signal))
        R5 = Rule(State.S4, State.S4, [str(i) for i in range(10)], lambda agent,signal: agent.update_status(signal))
        for el in rules:
            self.add_rule(el)


