import RPi.GPIO as GPIO
import time

class DistanceSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.TRIGGER_PIN = trigger_pin
        self.ECHO_PIN = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)

    def measure_distance(self):
        GPIO.output(self.TRIGGER_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIGGER_PIN, False)
        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.ECHO_PIN) == 0:
            start_time = time.time()

        while GPIO.input(self.ECHO_PIN) == 1:
            stop_time = time.time()

        elapsed_time = stop_time - start_time
        distance_cm = (elapsed_time * 34300) / 2
        print(f"Distance: {distance_cm} cm")
        return distance_cm

TRIGGER_PIN = 24
ECHO_PIN = 23

sensor_ult = DistanceSensor(TRIGGER_PIN, ECHO_PIN)
distance = sensor_ult.measure_distance()
