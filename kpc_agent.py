from finite_state_machine import State, FSM
class KpcAgent:
    def __init__(self):
        self.passwd_buffer = ""
        self.override_signal = False
        self.passwd="0000"
        self.fsm = FSM(self)

    def init_passcode_entry(self):
        self.passwd_buffer = ""
        self.twinkle_leds()

    def get_next_signal(self):
        if overwrite_signal:
            return self.verify_login()
        return input()

    def verify_login(self):

        self.override_signal=False
        self.passwd_buffer=""
        return self.passwd == self.passwd_buffer

    def validate_passcode_change(self):
        pass

    def light_one_led(self):
        pass

    def flash_leds(self):
        pass

    def twinkle_leds(self):
        pass

    def exit_action(self):
        pass

def main():
    agent = KpcAgent()
    while agent.fsm.state != State.S3:
        signal = agent.get_next_signal()
        agent.fsm.run_rules(signal)

    print("You are logged in")

