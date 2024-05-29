import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pwm_pin, 50)  # 50 Hz (20 ms PWM period)
        self.pwm.start(0)  # Initialization

    def set_angle(self, angle):
        duty_cycle = self.angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)  # Allow time for servo to move

    @staticmethod
    def angle_to_duty_cycle(angle):
        return 2 + (angle / 18)

    def move_to_max(self):
        self.set_angle(135)
        print("Moved to max position (180 degrees)")

    def move_to_min(self):
        self.set_angle(45)
        print("Moved to min position (0 degrees)")

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    SERVO_PIN = 26  

    motor = ServoMotor(SERVO_PIN)

    try:
        motor.move_to_max()
        time.sleep(2)
        motor.move_to_min()
    except KeyboardInterrupt:
        pass
    finally:
        motor.cleanup()
