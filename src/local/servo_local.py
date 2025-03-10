import serial
from openai import OpenAI
from time import sleep
import os
pico_port = "COM9"  # Adjust to your Pico’s port
ser = None

try:
    ser = serial.Serial(pico_port, 115200, timeout=1)
    print(f"Connected to {pico_port}")
except serial.SerialException as e:
    print(f"Failed to connect: {e}")
    exit(1)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"

def send_to_pico(command):
    if ser and ser.is_open:
        ser.write(f"{command}\n".encode())
        ser.flush()
        print(f"Sent to Pico: {command}")
        sleep(0.1)
        response = ser.readline().decode().strip()
        if response:
            print(f"Pico responded: {response}")
    else:
        print("Pico not connected!")

def get_openai_response(prompt):
    """Interpret user input for servo rotation commands"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a command interpreter for a servo motor. If the user asks to rotate (e.g., 'rotate 90 deg', 'can you rotate 90 degrees'), extract the angle (0-180) and respond with 'rotate X' where X is the angle. If no valid angle or command, respond with 'unknown'."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10
    )
    return response.choices[0].message.content.strip()

try:
    while True:
        user_input = input("Say something (e.g., 'can you rotate 90 deg'): ")
        command = get_openai_response(user_input)
        print(f"OpenAI returned: {command}")
        if command.startswith("rotate "):
            send_to_pico(command)
        else:
            print("Command not recognized.")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")