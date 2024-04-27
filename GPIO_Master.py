import RPi.GPIO as GPIO

class GPIOCtrl():
    def __init__(self):
        self.pin_ac1 = 17
        self.pin_ac2 = 27
        self.pin_fert = 22

        GPIO.setmode(GPIO.BCM)

        self.InitPin()
        self.TurnOff()

    def InitPin(self):
        GPIO.setup(self.pin_ac1, GPIO.OUT)
        GPIO.setup(self.pin_ac2, GPIO.OUT)
        GPIO.setup(self.pin_fert, GPIO.OUT)
        # pass

    def TurnOff(self):
        GPIO.output(self.pin_ac1, GPIO.HIGH)
        GPIO.output(self.pin_ac2, GPIO.HIGH)
        GPIO.output(self.pin_fert, GPIO.HIGH)
        # pass

    def TurnAc1(self):
        GPIO.output(self.pin_ac1, GPIO.LOW)
        # pass
    def TurnAc1Off(self):
        GPIO.output(self.pin_ac1, GPIO.HIGH)
        # pass

    def TurnAc2(self):
        GPIO.output(self.pin_ac2, GPIO.LOW)
        # pass
    def TurnAc2Off(self):
        GPIO.output(self.pin_ac2, GPIO.HIGH)
        # pass

    def TurnFert(self):
        GPIO.output(self.pin_fert, GPIO.LOW)
        # pass
    def TurnFertOff(self):
        GPIO.output(self.pin_fert, GPIO.HIGH)
        # pass

if __name__ == "__main__":
    GPIOCtrl()