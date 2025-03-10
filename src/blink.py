from machine import Pin
from time import sleep

# Set up the onboard LED on GPIO 25
led = Pin(25, Pin.OUT)

# Blink the LED
while True:
    led.on()   # Turn LED on
    sleep(1)   # Wait 1 second
    led.off()  # Turn LED off
    sleep(1)   # Wait 1 second