from finite_state_machine import State, FSM
from keypad import Keypad


class KpcAgent:
    def __init__(self):
        self.passwd_buffer = ""
        self.passwd_buffer2 = ""
        self.override_signal = False
        self.is_logged_in = False
        self.passwd = self.get_password_from_file()
        self.fsm = FSM(self)
        self.keypad = Keypad()

    def get_password_from_file(self):
        passwd = ""
        with open('passwd.txt') as passwd_file:
            passwd = passwd_file.readline().rstrip()
        return passwd

    def init_passcode_entry(self):
        self.passwd_buffer = ""
        self.twinkle_leds()

    def get_next_signal(self):
        if self.override_signal:
            return self.verify_login()
        return self.keypad.get_next_signal()

    def verify_login(self):

        print("verifying login")
        print("passwd_buffer", self.passwd_buffer)
        print("passwd", self.passwd)
        self.override_signal = False
        return self.passwd == self.passwd_buffer

    def validate_passcode_change(self, signal):
        if signal != '*':
            return
        if self.passwd_buffer == self.passwd_buffer2:
            print("Password is changed")
            self.passwd = self.passwd_buffer
            with open('passwd.txt', 'w') as passwd_file:
                passwd_file.write(self.passwd)
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
        self.override_signal = True

    def append_buffer(self, signal):
        self.passwd_buffer += signal

    def append_buffer2(self, signal):
        self.passwd_buffer2 += signal

    def reset_buffer(self, signal):
        self.passwd_buffer = ""

    def update_status(self, boolean):
        self.is_logged_in = boolean


if __name__ == "__main__":
    AGENT = KpcAgent()
    print("Starting machine")
    print("State: ", AGENT.fsm.state.value)
    while AGENT.fsm.state != State.S6:
        SIGNAL = AGENT.get_next_signal()
        AGENT.fsm.run_rules(SIGNAL)

    print("You are logged in")
