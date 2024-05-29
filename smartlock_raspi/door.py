import RPi.GPIO as GPIO

class DoorSensor:
    def __init__(self, pin):
        self.pin = pin
        self.door_active_state = False
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.pin, GPIO.IN)

    def door_state(self):
        try:
            GPIO.setmode(GPIO.BCM)  
            self.door_active_state = GPIO.input(self.pin)
            return self.door_active_state
        except KeyboardInterrupt:
            print("Door state checking interrupted.")
