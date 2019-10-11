from rule import Rule

class State(Enum)
    S0 = "inital state"
    S1 = "reading input"
    S2 = "verifying"
    S3 = "logged in"

class FSM:
    def __init__(self):
        self.curState = State.S0
        self.rules = []

    def add_rule(self):
        pass

    def get_next_signal(self):
        if(self.curState == State.S2)
            return
        return input()

    def run_rules(self):
        pass

    def apply_rule(self, rule):
        pass

    def fire_rule(self, rule):

        pass

    def main_loop(self):
        while self.curState != State.S3:
            signal = self.get_next_signal()
            for rule in self.rules:
                if apply_rule(rule, signal):
                    self.fire_rule(rule, signal)
	print("You are logged in")


    def gen_rules(self):
        # Inital state -> Reading
        R1 = Rule(State.S0, State.S1, [str(i) for i in range(10)], lambda agent,signal: agent.tmp_passwd+=signal)
        # Reading -> Verify
        R2 = Rule(State.S1, State.S2,'*', lambda agent, signal: agent.check_passwd())
        # Verify -> Init State
        R3 = Rule(State.S2, State.S0, False, lambda agent, signal: agent.tmp_passwd = "")
        # Verify -> logged in
        R4 = Rule(State.S2, State.S3, True, lambda agent,signal: agent.is_logged_in = True)
        rules = [R1,R2,R3,R4]
        for el in rules:
            self.add_rule(el)


