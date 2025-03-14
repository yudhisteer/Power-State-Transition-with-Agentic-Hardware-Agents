from fastapi import FastAPI, HTTPException
from time import sleep
import uvicorn
import logging
import colorlog
from gpiozero import AngularServo

# Set up logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    }
))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
app = FastAPI()

# Configure servo on GPIO 14 (your working setup)
servo = AngularServo(14, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

def set_angle(angle):
    """Set servo angle (0-180 degrees)"""
    servo.angle = angle
    sleep(1)  # Match your tested delay

@app.post("/rotate/")
async def rotate_servo(angle: int):
    try:
        if 0 <= angle <= 180:
            logger.info(f"Rotating servo to {angle}°")
            set_angle(angle)
            return {"status": f"Rotated to {angle}°"}
        else:
            raise HTTPException(status_code=400, detail="Angle must be between 0 and 180")
    except Exception as e:
        logger.error(f"Error rotating servo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def cleanup():
    servo.close()  # Properly close the servo object
    logger.info("Servo closed")

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.189.217", port=8000)