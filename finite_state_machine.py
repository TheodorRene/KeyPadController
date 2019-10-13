from enum import Enum
from rule import Rule


class State(Enum):
    S0 = "inital state"
    S1 = "reading input"
    S2 = "verifying"
    S3 = "logged in"
    S4 = "first password change"
    S5 = "second password change"
    S6 = "Exit"


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
            print("Current state: ", self.state.name)
        for rule in self.rules:
            if self.apply_rule(rule, signal):
                self.fire_rule(rule, signal)
                return
        print("Invalid char")
        self.change_state(State.S0)

    def apply_rule(self, rule, signal):
        if rule.trig_signals == ['all']:
            return True
        if self.state == rule.trig_state and signal in rule.trig_signals:
            return True
        return False

    def change_state(self, new_state):
        print("Changing state", self.state.value, " ->", new_state.value)
        self.state = new_state

    def fire_rule(self, rule, signal):
        rule.action(self.agent, signal)
        self.change_state(rule.new_state)
        print("New state: ", self.state.name)

    def gen_rules(self):
        # Inital state -> Reading
        R1 = Rule(State.S0,
                  State.S1,
                  [str(i) for i in range(10)],
                  lambda agent,
                  signal: agent.append_buffer(signal))
        # Reading -> Reading
        R1_1 = Rule(State.S1,
                    State.S1,
                    [str(i) for i in range(10)],
                    lambda agent,
                    signal: agent.append_buffer(signal))
        # Reading -> Verify
        R2 = Rule(
            State.S1,
            State.S2,
            ['*'],
            lambda agent,
            signal: agent.set_override_signal(signal))
        # Verify -> Init State
        R3 = Rule(
            State.S2,
            State.S0,
            [False],
            lambda agent,
            signal: agent.reset_buffer(signal))
        # Verify -> logged in
        R4 = Rule(
            State.S2,
            State.S3,
            [True],
            lambda agent,
            signal: agent.update_status(signal))
        # Verify -> Change password
        R5 = Rule(
            State.S3,
            State.S4,
            ['*'],
            lambda agent,
            signal: agent.reset_buffer(signal))
        # Change password -> Change password
        R6 = Rule(State.S4,
                  State.S4,
                  [str(i) for i in range(10)],
                  lambda agent,
                  signal: agent.append_buffer(signal))
        # Change password -> Change password 2
        R7 = Rule(State.S4, State.S5, ['*'], lambda agent, signal: None)
        # Change password 2 -> Change password 2
        R8 = Rule(State.S5,
                  State.S5,
                  [str(i) for i in range(10)],
                  lambda agent,
                  signal: agent.append_buffer2(signal))
        # Change password 2 -> Logged in
        R9 = Rule(
            State.S5,
            State.S3,
            ['all'],
            lambda agent,
            signal: agent.validate_passcode_change(signal))
        R10 = Rule(
            State.S3,
            State.S6,
            ['e'],
            lambda agent,
            signal: agent.validate_passcode_change(signal))

        rules = [R1, R1_1, R2, R3, R4, R5, R6, R7, R8, R9, R10]


        for el in rules:
            self.add_rule(el)
