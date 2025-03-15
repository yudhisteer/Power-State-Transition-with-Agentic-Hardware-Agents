import logging
import os
import requests
from openai import OpenAI

from util import logger_setup

# Initialize logger
logger = logging.getLogger(__name__)

# Server URL (replace with your Raspberry Pi's IP if different)
PI_API_URL = "http://192.168.189.217:8001/temperature/"

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def interpret_command(user_input: str) -> str:
    """Use OpenAI to determine if the user is asking for the temperature."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "If the user is asking for the temperature, respond with 'get_temperature'. Otherwise, respond with 'unknown'."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=10
        )
        command = response.choices[0].message.content.strip()
        logger.info(f"OpenAI response: {command}")
        return command
    except Exception as e:
        logger.error(f"Error interpreting command: {e}")
        return "unknown"

def fetch_temperature():
    """Fetch and display the temperature from the server."""
    try:
        response = requests.get(PI_API_URL)
        if response.status_code == 200:
            data = response.json()
            temp_c = data["celsius"]
            temp_f = data["fahrenheit"]
            logger.info(f"Temperature: {temp_c}°C / {temp_f}°F")
        else:
            logger.error(f"Server error: {response.json()['detail']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to server: {e}")

try:
    while True:
        user_input = input("Ask something (e.g., 'what is the temperature'): ")
        if user_input.lower() == "quit":
            logger.info("Quitting...")
            break
        command = interpret_command(user_input)
        if command == "get_temperature":
            logger.info("Fetching temperature...")
            fetch_temperature()
        else:
            logger.info("Command not recognized")
except KeyboardInterrupt:
    logger.info("\nExiting...")