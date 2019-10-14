import time

import RPi.GPIO as GPIO

class Keypad:
    def __init__(self):
        self.rows = []
        self.columns = []
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        self.rows = [18, 23, 24,25]
        self.columns = [17, 27, 22]
        for rp in self.rows:
            GPIO.setup(rp, GPIO.OUT)
        for cp in self.columns:
            GPIO.setup(cp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def do_polling(self):

        while True:

            for x, rp in enumerate(self.rows):
                GPIO.output(rp, GPIO.HIGH)
                for y, cp in enumerate(self.columns):
                    counter = 0
                    while GPIO.input(cp) == GPIO.HIGH:
                        counter += 1
                        time.sleep(0.005)
                    if counter >= 20: 
                        active = (x,y)
                        return self.coordinates_to_signal(active)
                    
                GPIO.output(rp, GPIO.LOW)
                
    def coordinates_to_signal(self, coords):
        mapping = {(0,0):'1', (0,1):'2', (0,2):'3',
                        (1,0):'4', (1,1):'5', (1,2):'6',
                        (2,0):'7', (2,1):'8', (2,2):'9',
                        (3,0):'*', (3,1):'0', (3,2):'#'}
        return mapping[coords]

    def get_next_signal(self):
        return self.do_polling()
if __name__=='__main__':
    kp = Keypad()
    while True:
        print(kp.get_next_signal())
