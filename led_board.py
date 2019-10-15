
import random
import time

import RPi.GPIO as GPIO
import keypad as kp




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

    def unlight_led(self):
        for i in range(3):
            self.set_pin(i, 0)

    def flash_all_leds(self, k):
        start = time.time()
        diff = 0
        pin = 0
        blink_time = 0.15
        while diff < k:
            tmp = time.time()
            tmp_diff = 0
            while tmp_diff < blink_time and diff < k:
                self.light_led(pin)
                diff = time.time() - start
                tmp_diff = time.time() - tmp
                pin = (pin + 1) % 6
            self.unlight_led()
            sleeptime = min(0.15, abs(k-diff))
            time.sleep(sleeptime)
            diff = time.time() - start
        self.unlight_led()

    def light_single_led(self, led_number, seconds):
        self.light_led(led_number)
        time.sleep(seconds)
        self.unlight_led()

    def twinkle_all_leds(self):
        for i in range(20):
            num = random.randint(0, 5)
            self.light_led(num)
            time.sleep(0.08)

        for i in range(3):
            self.set_pin(i, 0)



if __name__ == '__main__':
    LED = LEDboard()
    KEYPAD = kp.Keypad()
    while True:
        SIGNAL = int(KEYPAD.get_next_signal())
        print(SIGNAL)
        LED.light_led(SIGNAL)
