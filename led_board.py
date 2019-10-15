""" led board module """
import RPi.GPIO as GPIO
import keypad


class LEDboard:
    """Led board class"""
    def __init__(self):
        self.pins = []
        self.pin_led_states = []
        self.setup()
        self.set_pin(0, -1)
        self.set_pin(1, -1)
        self.set_pin(2, -1)

    def setup(self):
        """setup method"""
        self.pins = [5, 6, 13]
        self.pin_led_states = [
            [1, 0, -1],  # A
            [0, 1, -1],  # B
            [-1, 1, 0],  # C
            [-1, 0, 1],  # D
            [1, -1, 0],  # E
            [0, -1, 1]  # F
        ]
        GPIO.setmode(GPIO.BCM)

    def set_pin(self, pin_index, pin_state):
        """set pin method"""
        if pin_state == -1:
            GPIO.setup(self.pins[pin_index], GPIO.IN)
        else:
            GPIO.setup(self.pins[pin_index], GPIO.OUT)
            GPIO.output(self.pins[pin_index], pin_state)

    def light_led(self, led_number):
        """light_led method"""
        for pin_index, pin_state in enumerate(self.pin_led_states[led_number]):
            self.set_pin(pin_index, pin_state)

    def flash_all_leds(self):
        pass

    def twinkle_all_leds(self):
        pass


if __name__ == '__main__':
    LED = LEDboard()
    KEYPAD = keypad.Keypad()
    while True:
        SIGNAL = int(KEYPAD.get_next_signal())
        print(SIGNAL)
        LED.light_led(SIGNAL)
