import requests
from openai import OpenAI
import os
import logging
import colorlog

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


# Replace with Pi’s IP (same network) or Ngrok URL (different networks)
PI_API_URL = "http://192.168.189.217:8000/rotate/"

# OpenAI API configuration
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def interpret_command(user_input):
    """Use OpenAI to interpret the user's command and extract the angle."""
    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a command interpreter for a servo motor. Extract the angle (0-180 degrees) from the user's request. Respond with 'rotate X' where X is the angle, or 'unknown' if the command is invalid."},
            {"role": "user", "content": user_input}
        ],
            max_tokens=10
        )
        logger.info(f"OpenAI response: {response.choices[0].message.content.strip()}")
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error interpreting command: {e}")
        return "unknown"

def send_to_pi(angle):
    """Send the angle to the Raspberry Pi's API."""
    try:
        response = requests.post(PI_API_URL, params={"angle": angle})
        if response.status_code == 200:
            logger.info(f"Pi responded: {response.json()['status']}")
        else:
            logger.error(f"Error: {response.json()['detail']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to Pi: {e}")

try:
    while True:
        user_input = input("Say something (e.g., 'rotate the servo to 90 degrees'): ")
        if user_input.lower() == "quit":
            logger.info("Quitting...")
            break
        command = interpret_command(user_input)
        if command.startswith("rotate "):
            logger.info(f"Command: {command}")
            try:
                angle = int(command.split(" ")[1])
                if 0 <= angle <= 180:
                    logger.info(f"Sending angle to Pi: {angle}")
                    send_to_pi(angle)
                else:
                    logger.error("Angle must be between 0 and 180")
            except ValueError:
                logger.error("Invalid angle received from OpenAI")
        else:
            logger.error("Command not recognized by OpenAI")
except KeyboardInterrupt:
    logger.info("\nExiting...")