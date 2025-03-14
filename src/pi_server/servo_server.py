# servo_fastapi.py (on Raspberry Pi 5)
from fastapi import FastAPI, HTTPException
import RPi.GPIO as GPIO
import time
import uvicorn

app = FastAPI()

# Configure PWM pin for servo (GPIO 14)
SERVO_PIN = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz for servos
servo.start(0)

def set_servo_angle(angle):
    duty = 2.5 + (angle * 10.0 / 180)  # Convert angle to duty cycle
    servo.ChangeDutyCycle(duty)
    time.sleep(0.1)
    servo.ChangeDutyCycle(0)

@app.post("/rotate/")
async def rotate_servo(angle: int):
    if 0 <= angle <= 180:
        set_servo_angle(angle)
        return {"status": f"Rotated to {angle}°"}
    else:
        raise HTTPException(status_code=400, detail="Angle must be between 0 and 180")

@app.on_event("shutdown")
def cleanup():
    servo.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)