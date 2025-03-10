from machine import Pin, PWM
import time

# Configure PWM pin (adjust pin number based on your board)
SERVO_PIN = 0  # GP0 on Pico, GPIO13 on ESP32, etc.
servo = PWM(Pin(SERVO_PIN))
servo.freq(50)  # 50Hz is standard for servos

def set_servo_angle(angle):
    """Set servo angle (0-180 degrees)"""
    # MicroPython PWM duty is 0-65535; servo range is ~1638 (0°) to ~8192 (180°)
    duty = int(1638 + (angle * (8192 - 1638) / 180))
    servo.duty_u16(duty)
    time.sleep(0.1)  # Allow servo to settle

# Main loop for real-time control
print("Enter angle (0-180) or 'q' to quit")
while True:
    try:
        user_input = input("> ")
        if user_input.lower() == 'q':
            break
        angle = int(user_input)
        if 0 <= angle <= 180:
            print(f"Moving to {angle}°")
            set_servo_angle(angle)
        else:
            print("Angle must be 0-180")
    except ValueError:
        print("Enter a valid number or 'q'")
        
servo.deinit()  # Clean up