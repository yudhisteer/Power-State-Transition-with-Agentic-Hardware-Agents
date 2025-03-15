import glob
import logging
import time

import uvicorn
from fastapi import FastAPI, HTTPException

from util import logger_setup

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Locate the DS18B20 sensor device file
base_dir = "/sys/bus/w1/devices/"
try:
    device_folder = glob.glob(base_dir + "28*")[0]
    device_file = device_folder + "/w1_slave"
    logger.info(f"Device file: {device_file}")
except IndexError:
    logger.error("No DS18B20 device found")
    device_file = None

def read_temp_raw():
    """Read raw data from the sensor's w1_slave file."""
    if device_file is None:
        raise Exception("Temperature sensor not found")
    with open(device_file, "r") as f:
        lines = f.readlines()
    logger.info(f"Raw temperature data: {lines}")
    return lines

def read_temp():
    """Process raw data to extract temperature in Celsius and Fahrenheit."""
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != "YES":  # Wait for a valid reading
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        logger.info(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
        return round(temp_c, 2), round(temp_f, 2)
    else:
        logger.error("Invalid temperature data")
        raise Exception("Invalid temperature data")

@app.get("/temperature/")
async def get_temperature():
    """Endpoint to return the current temperature."""
    try:
        temp_c, temp_f = read_temp()
        logger.info(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
        return {"celsius": temp_c, "fahrenheit": temp_f}
    except Exception as e:
        logger.error(f"Error reading temperature: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.189.217", port=8000)