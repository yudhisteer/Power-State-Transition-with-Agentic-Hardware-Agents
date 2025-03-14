import serial
from openai import OpenAI
from time import sleep
import os
pico_port = "COM9"
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
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a simple command interpreter. If the user says 'blink', respond with 'blink'. Otherwise, respond with 'unknown'."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10
    )
    return response.choices[0].message.content.strip()

try:
    while True:
        user_input = input("Say something (e.g., 'blink'): ")
        command = get_openai_response(user_input)
        print(f"OpenAI returned: {command}")
        if command == "blink":
            send_to_pico("blink")
        else:
            print("Command not recognized.")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")