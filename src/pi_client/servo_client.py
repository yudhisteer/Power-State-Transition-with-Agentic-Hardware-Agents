import requests
from openai import OpenAI
import os

# Replace with Pi’s IP (same network) or Ngrok URL (different networks)
PI_API_URL = "http://<pi-ip-or-ngrok-url>:5000/rotate/"

# OpenAI API configuration
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def interpret_command(user_input):
    """Use OpenAI to interpret the user's command and extract the angle."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a command interpreter for a servo motor. Extract the angle (0-180 degrees) from the user's request. Respond with 'rotate X' where X is the angle, or 'unknown' if the command is invalid."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=10
    )
    return response.choices[0].message.content.strip()

def send_to_pi(angle):
    """Send the angle to the Raspberry Pi's API."""
    try:
        response = requests.post(PI_API_URL, json={"angle": angle})
        if response.status_code == 200:
            print(f"Pi responded: {response.json()['status']}")
        else:
            print(f"Error: {response.json()['detail']}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Pi: {e}")

try:
    while True:
        user_input = input("Say something (e.g., 'rotate the servo to 90 degrees'): ")
        if user_input.lower() == "quit":
            break
        command = interpret_command(user_input)
        if command.startswith("rotate "):
            try:
                angle = int(command.split(" ")[1])
                if 0 <= angle <= 180:
                    send_to_pi(angle)
                else:
                    print("Angle must be between 0 and 180")
            except ValueError:
                print("Invalid angle received from OpenAI")
        else:
            print("Command not recognized by OpenAI")
except KeyboardInterrupt:
    print("\nExiting...")