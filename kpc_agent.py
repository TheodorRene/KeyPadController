"""keypad controller agent module"""
from finite_state_machine import State, FSM
from keypad import Keypad
from led_board import LEDboard


class KpcAgent:
    """Keypad controller agent class"""
    def __init__(self):
        self.passwd_buffer = ""
        self.passwd_buffer2 = ""
        self.override_signal = False
        self.is_logged_in = False
        self.passwd = self.get_password_from_file()
        self.fsm = FSM(self)
        self.keypad = Keypad()
        self.led_board = LEDboard()
        self.initiated = False
        self.led = -1

    def get_password_from_file(self):
        """get password from file"""
        passwd = ""
        with open('passwd.txt') as passwd_file:
            passwd = passwd_file.readline().rstrip()
        return passwd

    def init_passcode_entry(self, signal):
        """empty passwordbuffer and blinks leds"""
        self.passwd_buffer += signal
        if not self.initiated:
            self.twinkle_all_leds()
        self.initiated = True

    def get_next_signal(self):
        """gets next signal from keypad if not last signal was *"""
        if self.override_signal:
            return self.verify_login()
        return self.keypad.get_next_signal()

    def verify_login(self):
        """verify login"""
        print("verifying login")
        print("passwd_buffer", self.passwd_buffer)
        print("passwd", self.passwd)
        self.override_signal = False
        buff = self.passwd_buffer
        self.reset_buffer(None)
        return self.passwd == buff

    def validate_passcode_change(self, signal):
        """validates password change"""
        if signal != '*':
            return
        if self.passwd_buffer == self.passwd_buffer2:
            print("Password is changed")
            self.passwd = self.passwd_buffer
            with open('passwd.txt', 'w') as passwd_file:
                passwd_file.write(self.passwd)
        return

    def light_one_led(self, signal):
        if self.led == -1:
            self.led = int(signal)
            return
        self.led_board.light_single_led(self.led, int(self.passwd_buffer))

    def flash_all_leds(self, signal):
        print("===FLASHING ALL LEDS===")
        self.led_board.flash_all_leds(3)

    def twinkle_all_leds(self):
        print("===TWINKLING LEDS===")
        self.led_board.twinkle_all_leds()

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
        self.led_board.light_sequence([0, 4, 2], 0.3)
    
    def logout_lightshow(self, signal):
        self.led_board.light_sequence([1,2,3,3,2,1],0.2)


if __name__ == "__main__":
    AGENT = KpcAgent()
    print("Starting machine")
    print("State: ", AGENT.fsm.state.value)
    while AGENT.fsm.state != State.S9:
        SIGNAL = AGENT.get_next_signal()
        print(SIGNAL)
        AGENT.fsm.run_rules(SIGNAL)

    print("You are logged in")
