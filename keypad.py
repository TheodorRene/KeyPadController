"""keypad module"""
import time
import RPi.GPIO as GPIO


class Keypad:
    """Keypad class translates the position on the keypad into the numbers that are visualised"""
    def __init__(self):
        self.rows = []
        self.columns = []
        self.setup()

    def setup(self):
        """setup"""
        GPIO.setmode(GPIO.BCM)
        self.rows = [18, 23, 24, 25]
        self.columns = [17, 27, 22]
        for row in self.rows:
            GPIO.setup(row, GPIO.OUT)
        for col in self.columns:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def do_polling(self):
        """do_polling"""
        while True:
            for coor_x, row in enumerate(self.rows):
                GPIO.output(row, GPIO.HIGH)
                for coor_y, col in enumerate(self.columns):
                    counter = 0
                    while GPIO.input(col) == GPIO.HIGH:
                        counter += 1
                        time.sleep(0.005)
                    if counter >= 20:
                        active = (coor_x, coor_y)
                        return self.coordinates_to_signal(active)

                GPIO.output(row, GPIO.LOW)

    @staticmethod
    def coordinates_to_signal(coords):
        """coordinates to signal"""
        mapping = {(0, 0): '1', (0, 1): '2', (0, 2): '3',
                   (1, 0): '4', (1, 1): '5', (1, 2): '6',
                   (2, 0): '7', (2, 1): '8', (2, 2): '9',
                   (3, 0): '*', (3, 1): '0', (3, 2): '#'}
        return mapping[coords]

    def get_next_signal(self):
        """get next signal"""
        return self.do_polling()


if __name__ == '__main__':
    KEY_PAD = Keypad()
    while True:
        print(KEY_PAD.get_next_signal())
