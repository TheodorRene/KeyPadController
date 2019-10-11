from enum  import Enum

class State(Enum)
    S0 = "inital state"
    S1 = "reading input"
    S2 = "verifying"
    S3 = "logged in"

class FSM:
    def __init__(self, agent):
        self.state = State.S0
        self.rules = []
        self.gen_rules()
        self.agent = agent

    def add_rule(self, rule):
        self.rules.append(rule)

    def run_rules(self, signal):
        for rule in self.rules:
            if self.apply_rule(rule, signal):
                self.fire_rule(rule, signal)

    def apply_rule(self, rule, signal):
        if self.state == rule.trig_state and signal in rule.trig_signals:
            return True
        return False

    def fire_rule(self, rule, signal):
        rule.action(self.agent, signal)

    def gen_rules(self):
        # Inital state -> Reading
        R1 = Rule(State.S0, State.S1, [str(i) for i in range(10)], lambda agent,signal: agent.tmp_passwd+=signal)
        # Reading -> Verify
        R2 = Rule(State.S1, State.S2,['*'], lambda agent, signal: agent.overwride_signal=True)
        # Verify -> Init State
        R3 = Rule(State.S2, State.S0, [False], lambda agent, signal: agent.tmp_passwd = "")
        # Verify -> logged in
        R4 = Rule(State.S2, State.S3, [True], lambda agent,signal: agent.is_logged_in = True)
        rules = [R1,R2,R3,R4]
        for el in rules:
            self.add_rule(el)


