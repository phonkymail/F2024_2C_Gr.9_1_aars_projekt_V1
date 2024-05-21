import time
from rpi_ws281x import PixelStrip, Color

class LedRGB:
    def __init__(self):
# LED strip configuration:
        self.LED_COUNT = 2       
        self.LED_PIN = 13           
        self.LED_FREQ_HZ = 800000      
        self.LED_DMA = 10                
        self.LED_BRIGHTNESS = 255       
        self.LED_INVERT = False         
        self.LED_CHANNEL = 1             
        self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        self.strip.begin()
#method turn on colour cons.
    def set_color(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
#method turn on colour blink
    def blink_rgb(self, color, delay):
        """Blink LEDs in sequence with the specified color and delay."""
        for i in range(self.strip.numPixels()):
            # Turn on current LED
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(delay)

            # Turn off current LED
            self.strip.setPixelColor(i, Color(0, 0, 0))
            self.strip.show()

#--------------------------------------------------------------------
#creae object
time.sleep(5)
led_rgb = LedRGB()
led_rgb.set_color(Color(255,255,255))
time.sleep(3)

# Uruchom sekwencję migania diodami w kolorze czerwonym, opóźnienie 0.5 sekundy
led_rgb.blink_rgb(Color(255, 0, 0), 0.5)

# Wyłącz diody
led_rgb.set_color(Color(0, 0, 0))

