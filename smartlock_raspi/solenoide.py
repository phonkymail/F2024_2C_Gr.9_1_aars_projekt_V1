import RPi.GPIO as GPIO
import smbus2
import pigpio
from time import sleep


#create class
class MosfetController:
    def __init__(self, pin):
        self.fet_pin = pin
        self.pwm_frequency = 1000
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.fet_pin, GPIO.OUT)
        self.pwm_fet = GPIO.PWM(self.fet_pin, self.pwm_frequency)
        self.pwm_fet.start(0)
 #create method   
    def set_duty(self, duty):
        self.pwm_fet.ChangeDutyCycle(duty)
        self.current_duty = duty  # Update current duty cycle
    


