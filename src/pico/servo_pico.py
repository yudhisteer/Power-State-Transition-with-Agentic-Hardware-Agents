from machine import Pin, PWM
import time
import sys

# Configure PWM pin for servo (GP0 on Pico)
SERVO_PIN = 0
servo = PWM(Pin(SERVO_PIN))
servo.freq(50)  # 50Hz standard for servos

def set_servo_angle(angle):
    """Set servo angle (0-180 degrees)"""
    # PWM duty_u16 range: ~1638 (0°) to ~8192 (180°)
    duty = int(1638 + (angle * (8192 - 1638) / 180))
    servo.duty_u16(duty)
    time.sleep(0.1)  # Allow servo to settle

# Main loop for serial input
print("Servo control started")
while True:
    line = sys.stdin.readline().strip()
    print(f"Received: {line}")
    if line.startswith("rotate "):
        try:
            angle = int(line.split(" ")[1])  # Extract number after "rotate"
            if 0 <= angle <= 180:
                print(f"Rotating to {angle}°")
                set_servo_angle(angle)
            else:
                print("Angle must be 0-180")
        except (ValueError, IndexError):
            print("Invalid rotate command")

servo.deinit()  # Clean up (won’t reach here unless loop breaks)