"""finite state machine module"""
from enum import Enum
from rule import Rule


class State(Enum):
    """State subclass of superclass Enum"""
    S0 = "inital state"
    S1 = "reading input"
    S2 = "verifying"
    S3 = "logged in"
    S4 = "first password change"
    S5 = "second password change"
    S6 = "Choose LED"
    S7 = "Choose duration"
    S8 = "Begin logout"
    S9 = "Logout"



class FSM:
    """Finite state machine class keeping track of what state the system is in"""
    def __init__(self, agent):
        self.state = State.S0
        self.rules = []
        self.agent = agent
        self.gen_rules()
        self.debug = True

    def add_rule(self, rule):
        self.rules.append(rule)

    def run_rules(self, signal):
        if self.debug:
            print("Current state: ", self.state.name)
        for rule in self.rules:
            if self.apply_rule(rule, signal):
                print("APPLYING RULE")
                self.fire_rule(rule, signal)
                return
        print("Invalid char")
        self.change_state(State.S0)

    def apply_rule(self, rule, signal):
        if self.state == rule.trig_state and signal in rule.trig_signals:
            return True
        #if rule.trig_signals == ['all']:
        #    return True
        return False

    def change_state(self, new_state):
        print("Changing state", self.state.value, " ->", new_state.value)
        self.state = new_state

    def fire_rule(self, rule, signal):
        print("Fire rule: ",rule.name)
        rule.action(signal)
        self.change_state(rule.new_state)
        print("New state: ", self.state.name)

    def gen_rules(self):
        # Inital state -> Reading
        rule1 = Rule(State.S0,
                     State.S1,
                     [str(i) for i in range(10)],
                     self.agent.init_passcode_entry,
                     "rule1")
        # Reading -> Reading
        rule1_1 = Rule(State.S1,
                       State.S1,
                       [str(i) for i in range(10)],
                       self.agent.append_buffer,
                       "rule1_1")
        # Reading -> Verify
        rule2 = Rule(
            State.S1,
            State.S2,
            ['*'],
            self.agent.set_override_signal,"rule2")
        # Verify -> Init State
        rule3 = Rule(
            State.S2,
            State.S0,
            [False],
            self.agent.flash_all_leds, "rule3")
        # Verify -> logged in
        rule4 = Rule(
            State.S2,
            State.S3,
            [True],
            self.agent.update_status, "rule4")
        # Logged in -> Change password
        rule5 = Rule(
            State.S3,
            State.S4,
            ['*'],
            self.agent.reset_buffer, "rule5")
        # Change password -> Change password
        rule6 = Rule(State.S4,
                     State.S4, [str(i) for i in range(10)], self.agent.append_buffer, "rule6")
        # Change password -> Change password 2
        rule7 = Rule(State.S4, State.S5, ['*'], lambda signal: None, "rule7")
        # Change password 2 -> Change password 2
        rule8 = Rule(State.S5,
                     State.S5, [str(i) for i in range(10)],
                     self.agent.append_buffer2,
                     "rule8")
        # Change password 2 -> Logged in
        rule9 = Rule(
            State.S5,
            State.S3,
            ['all'],
            self.agent.validate_passcode_change,
            "rule9")
        # Logged in -> Choose Led
        rule10 = Rule(
            State.S3,
            State.S6,
            [str(i) for i in range(10)],
            self.agent.light_one_led,
            "rule10"
        )
        # Choose Led -> Choose duration
        rule11 = Rule(
            State.S6,
            State.S7,
            ['*'],
            self.agent.reset_buffer,
            "rule11")
        # Choose duration -> Choose duration
        rule12 = Rule(
            State.S7,
            State.S7,
            [str(i) for i in range(10)],
            self.agent.append_buffer,
            "rule12")
        # Choose duration -> Logged in
        rule13 = Rule(
            State.S7,
            State.S3,
            ['*'],
            self.agent.light_one_led,
            "rule13")
        # logged in -> begin log out
        rule14 = Rule(
            State.S3,
            State.S8,
            ['#'],
            lambda signal: None,
            "rule14")
        # Begin log out -> Logout
        rule15 = Rule(
            State.S8,
            State.S9,
            ['#'],
            self.agent.logout_lightshow,
            "rule15")


        rules = [rule1, rule1_1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15]

        for rule in rules:
            self.add_rule(rule)
