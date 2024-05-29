import RPi.GPIO as GPIO
import time

class DistanceSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.TRIGGER_PIN = trigger_pin
        self.ECHO_PIN = echo_pin
        GPIO.setwarnings(False)  
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)

    def measure_distance(self):
        GPIO.output(self.TRIGGER_PIN, False)
        time.sleep(0.2)  
        
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
        print(f"Distance: {distance_cm:.0f} cm")
        return distance_cm

    def cleanup(self):
        GPIO.cleanup()


