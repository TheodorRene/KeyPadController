import RPi.GPIO as GPIO
import keypad as kp

class LEDboard:

    def __init__(self):
        self.pins = []
        self.pin_led_states = []
        self.setup()
        self.set_pin(0, -1)
        self.set_pin(1, -1)
        self.set_pin(2, -1)

    def setup(self):
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
        if pin_state == -1:
            GPIO.setup(self.pins[pin_index], GPIO.IN)
        else:
            GPIO.setup(self.pins[pin_index], GPIO.OUT)
            GPIO.output(self.pins[pin_index], pin_state)

    def light_led(self, led_number):
        for pin_index, pin_state in enumerate(self.pin_led_states[led_number]):
            self.set_pin(pin_index, pin_state)

    def flash_all_leds(self):
        pass

    def twinkle_all_leds(self):
        pass

if __name__ == '__main__':
    led = LEDboard()
    keypad = kp.Keypad()
    while True:
        x = int(keypad.get_next_signal())
        print(x)
        led.light_led(x)
