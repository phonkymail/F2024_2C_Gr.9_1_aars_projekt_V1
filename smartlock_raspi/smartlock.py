import paho.mqtt.client as mqtt
import base64
import os
from time import sleep
from picamera import PiCamera
from ultra import DistanceSensor
from led import LedRGB
from rpi_ws281x import Color
from motor import ServoMotor
from door import DoorSensor
from smbus import SMBus
from lib_oled96 import ssd1306
from solenoide import MosfetController


#
broker_address = "192.168.43.144"
port = 1883
topic_rasp = "image"
topic_server = "recognition"
client_id = "raspi"
image_folder = "/home/rav/Desktop/1ars/smartlock/new/"
os.makedirs(image_folder, exist_ok=True)
# 
TRIGGER_PIN = 15
ECHO_PIN = 14
SERVO_PIN = 26  
Doorsensor_PIN = 23
solenodie_PIN = 5
door_PIN = 23
# 
sensor_ult = DistanceSensor(TRIGGER_PIN, ECHO_PIN)
led_rgb = LedRGB()
door_sensor = DoorSensor(Doorsensor_PIN)
motor = ServoMotor(SERVO_PIN)
i2cbus = SMBus(1) 
oled = ssd1306(i2cbus)
pumpe_controller = MosfetController(solenodie_PIN)


#
message_received = False
message_payload = ""

#
def turnoff_display():
    oled.onoff(0)
def text_display(line1_text, line1_pos, line2_text, line2_pos, line3_text, line3_pos):
    oled.canvas.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0) 
    oled.canvas.text(line1_pos, line1_text, fill=1)  # Line 1
    oled.canvas.text(line2_pos, line2_text, fill=1)  # Line 2
    oled.canvas.text(line3_pos, line3_text, fill=1)  # Line 3
    oled.display()
# 
def capture_images(image_folder, num_images, delay):
    camera = PiCamera()
    camera.resolution = (640, 480)
    text_display('not move', (40, 5), 'take photo', (40, 25), 'in 5 sec', (40, 45))
    print("Capturing images...in 5sec")
    sleep(5)
    for i in range(num_images):
        image_path = os.path.join(image_folder, f"image_{i}.jpg")
        camera.capture(image_path)
        print(f"Captured {image_path}")
        sleep(delay)
    camera.close()

# 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic_server)
    else:
        print(f"Failed to connect, return code {rc}\n")

# 
def on_message(client, userdata, msg):
    global message_received, message_payload
    try:
        message = msg.payload.decode()
        print(f"Received message on {msg.topic}: {message}")
        message_received = True
        message_payload = message
    except Exception as e:
        print(f"Error decoding message: {e}")

# 
def publish_image(image_path, client):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        file_name = os.path.basename(image_path)
        payload = f"{file_name}:{encoded_image}"
        client.publish(topic_rasp, payload)
        print(f"Published {file_name} to {topic_rasp}")
    except Exception as e:
        print(f"Error encoding or publishing image: {e}")

def close_door():
    while True:
        door_state = door_sensor.door_state()
        if door_state == 0:
            print("Door open")
            text_display('close', (40, 5), 'door', (40, 25), 'to continue', (40, 45))

            sleep(1) 
        else:
            print("Door closed, proceeding with the rest of the code")
            break

def measure_distance_loop():
    while True:
        close_door()


        distance = sensor_ult.measure_distance()
        print(f"Distance: {distance} cm")
        if distance >= 80:
            led_rgb.set_color(Color(0, 0, 0))
            
        # Distance under 80 cm
        if distance < 80:
            led_rgb.set_color(Color(255, 255, 255))
            text_display('welcome', (40, 5), 'come closer', (40, 25), 'to camera', (40, 45))
        # Distance under 40 cm
        if distance < 40:
            # 
            capture_images(image_folder, 3, 0.5)
            led_rgb.set_color(Color(0, 0, 60))
            sleep(3)
            text_display('please', (40, 5), 'wait', (40, 25), 'processing', (40, 45))
            #
            client = mqtt.Client(client_id)
            #
            client.on_connect = on_connect
            client.on_message = on_message
            #
            client.connect(broker_address, port)
            sleep(0.5)
            # 
            client.loop_start()
            # 
            for file in os.listdir(image_folder):
                image_path = os.path.join(image_folder, file)
                publish_image(image_path, client)
                sleep(0.5)

            print("Finished publishing images. Waiting for responses...")

            # 
            global message_received, message_payload
            message_received = False
            while not message_received:
                sleep(0.1)

            # 
            if message_payload == "no permission":
                led_rgb.set_color(Color(255, 0, 0))  # Red color
                text_display('you dont', (40, 5), 'have', (40, 25), 'permission', (40, 45))

                sleep(15)
            else:
                text_display('welcome', (40, 5), 'you have', (40, 25), 'come in', (40, 45))
                led_rgb.set_color(Color(0, 255, 0))  # Green color
                pumpe_controller.set_duty(80)
                sleep(2)
                motor.move_to_max()
                sleep(10)
                pumpe_controller.set_duty(80)
                sleep(2)
                motor.move_to_min()                 
                led_rgb.set_color(Color(0, 0, 0))  # Turn off LED
                turn_off_display() #turn off display


            client.loop_stop()
            client.disconnect()
        sleep(3)

# 
def main():
    measure_distance_loop()

if __name__ == "__main__":
    main()
