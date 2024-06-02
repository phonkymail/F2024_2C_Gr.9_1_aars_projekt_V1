import time
from rpi_ws281x import PixelStrip, Color

class LedRGB:
    def __init__(self):
# 
        self.LED_COUNT = 3       
        self.LED_PIN = 13           
        self.LED_FREQ_HZ = 800000      
        self.LED_DMA = 10                
        self.LED_BRIGHTNESS = 255       
        self.LED_INVERT = False         
        self.LED_CHANNEL = 1             
        self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        self.strip.begin()
#
    def set_color(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

#
    def blink_sequence(self, color, delay):
        for _ in range(5):  # Repeat the sequence 5 times
            for i in range(self.strip.numPixels()):
                # Turn on current LED
                self.strip.setPixelColor(i, color)
                self.strip.show()
                time.sleep(delay)

                # Turn off current LED
                self.strip.setPixelColor(i, Color(0, 0, 0))
                self.strip.show()
                time.sleep(delay)

#--------------------------------------------------------------------
#led_rgb = LedRGB()
#led_rgb.blink_sequence(Color(255, 0, 0), 0.5)



