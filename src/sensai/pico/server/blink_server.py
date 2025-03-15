import sys
from time import sleep

from machine import Pin

led = Pin(25, Pin.OUT)  # Adjust to your LED pin (e.g., 16 for external)

while True:
    line = sys.stdin.readline().strip()
    print(f"Received: {line}")  # Debug output
    if line == "blink":
        for _ in range(5):
            led.on()
            sleep(0.5)
            led.off()
            sleep(0.5)