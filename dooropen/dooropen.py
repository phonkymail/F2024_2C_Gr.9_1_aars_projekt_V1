from time import sleep
import RPi.GPIO as GPIO

class DoorSensor:
    def __init__(self, pin):
        self.pin = pin
        self.door_active_state = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.setwarnings(False)
    def door_active(self):
        try:
            while True:
                self.door_active_state = GPIO.input(self.pin)
                print("Door Active =", self.door_active_state)
                if self.door_active_state == False:
                    sleep(0.05)
                    if self.door_active_state == False:
                        print("Switch state FALSE, door is open")
                else:
                    sleep(0.05)
                    if self.door_active_state == True:
                        print("Switch state TRUE, door is closed!")
                sleep(2)

        except KeyboardInterrupt:
            GPIO.cleanup() 
door_sensor = DoorSensor(27)
door_sensor.door_active()
