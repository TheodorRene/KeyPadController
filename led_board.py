import random
import time

import RPI.GPIO as GPIO
import keypad as kp


class LEDboard:

    def __init__(self):
        self.pins = []
        self.pin_led_states = []
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

    def flash_all_leds(self, k):
        start = time.time()
        diff = 0
        pin = 0
        while diff < k:
            self.light_led(pin)
            diff = time.time() - start
            pin = (pin + 1) % 6
        for i in range(3):
            self.set_pin(i, 0)

    def twinkle_all_leds(self):
        for i in range(20):
            num = random.randint(0, 5)
            self.light_led(num)
            time.sleep(0.08)

        for i in range(3):
            self.set_pin(i, 0)


if __name__ == '__main__':
    led = LEDboard()
    keypad = kp.Keypad()
    while True:
        x = int(keypad.get_next_signal())
        led.light_led(x)
