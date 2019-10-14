import RPi.GPIO as GPIO

class Keypad:

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        self.rows = [18, 23, 24,25]
        self.columns = [17, 27, 22]
        for rp in rows:
            GPIO.setup(rp, GPIO.OUT)
        for cp in columns:
            GPIO.setup(cp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        pass

    def do_polling(self):
        while True:
            for rp in self.rows:
                GPIO.output(rp, GPIO.HIGH):
                    for cp in self.column:
                        if GPIO.input(cp) == GPIO.HIGH:
                            active = (rp,cp)
                            return coordinates_to_signal(active)
                GPIO.output(rp, GPIO.LOW):
    def coordinates_to_signal(coords):
        mapping = {(0,0):1, (0,1):2, (0,2):3,
                        (1,0):4, (1,1):5, (1:2):6,
                        (2:0):7, (2:1):8, (2:2):9,
                        (3:0):'*', (3:1):0, (3:2):'#'}
        return mapping[coords]

    def get_next_signal(self):
        return do_polling
