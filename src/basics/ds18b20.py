import glob
import time
import logging

from util import logger_setup
logger = logging.getLogger(__name__)

try:
    # Path to the directory containing device files for 1-wire devices
    base_dir = "/sys/bus/w1/devices/"
    # Find the first device folder that starts with "28", specific to DS18B20
    device_folder = glob.glob(base_dir + "28*")[0]
except IndexError:
    logger.error("No DS18B20 device found") 

# Device file containing the temperature data
device_file = device_folder + "/w1_slave"

def read_temp_raw():
    # Read raw temperature data from the sensor
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()
    logger.debug(f"Raw temperature data: {lines}")
    return lines

def read_temp():
    # Parse the raw temperature data and convert it to Celsius and Fahrenheit
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find("t=")
    logger.debug(f"Temperature data: {lines[1]}")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        logger.debug(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
        return round(temp_c, 2), round(temp_f, 2)

while True:
    temp_c, temp_f = read_temp()
    print(temp_c, temp_f)
    print(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
    time.sleep(1)
