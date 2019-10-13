from finite_state_machine import State, FSM
class KpcAgent:
    def __init__(self):
        self.passwd_buffer = ""
        self.passwd_buffer2 = ""
        self.override_signal = False
        self.passwd="0000"
        self.fsm = FSM(self)

    def init_passcode_entry(self):
        self.passwd_buffer = ""
        self.twinkle_leds()

    def get_next_signal(self):
        if self.override_signal:
            return self.verify_login()
        return input()

    def verify_login(self):

        print("verifying login")
        print("passwd_buffer", self.passwd_buffer)
        print("passwd", self.passwd)
        self.override_signal=False
        return self.passwd == self.passwd_buffer

    def validate_passcode_change(self, signal):
        if signal != '*':
            return
        if self.passwd_buffer == self.passwd_buffer2:
            print("Password is changed")
            self.passwd = self.passwd_buffer
        return

    def light_one_led(self):
        pass

    def flash_leds(self):
        pass

    def twinkle_leds(self):
        pass

    def exit_action(self):
        pass

    def set_override_signal(self, signal):
        self.override_signal=True

    def append_buffer(self, signal):
        self.passwd_buffer+=signal

    def append_buffer2(self, signal):
        self.passwd_buffer2+=signal

    def reset_buffer(self, signal):
        self.passwd_buffer=""

    def update_status(self, boolean):
        self.is_logged_in = boolean

if __name__=="__main__":
    agent = KpcAgent()
    print("Starting machine")
    print("State: ", agent.fsm.state.value)
    while agent.fsm.state != State.S6:
        signal = agent.get_next_signal()
        agent.fsm.run_rules(signal)

    print("You are logged in")

