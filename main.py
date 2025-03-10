# Windows PC side (main.py)
import openai
import serial
import time
import os
from openai import OpenAI

# Configure your OpenAI API key
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Configure the serial connection to your Pico
# Change COM port as needed - check Device Manager to find the right port
ser = serial.Serial('COM9', 115200, timeout=2)
time.sleep(2)  # Give the connection time to establish

def get_command():
    """Get a command from the user via console input"""
    return input("Enter command (e.g., 'blink', 'on', 'off', 'exit'): ")

def process_command_with_openai(user_input):
    """Process user input with OpenAI API to determine the command"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a controller for a Raspberry Pi Pico. "
                 "Interpret user commands and respond ONLY with one of these exact words: "
                 "'blink', 'on', 'off', 'unknown'. Do not include any other text."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=10
        )
        command = response.choices[0].message.content.strip().lower()
        print(f"OpenAI interpreted your command as: {command}")
        
        # Validate the command
        if command in ['blink', 'on', 'off']:
            return command
        return "unknown"
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "unknown"

def main():
    print("Voice-Controlled Pico System")
    print("----------------------------")
    print("Type commands or phrases, and OpenAI will interpret them.")
    
    while True:
        user_input = get_command()
        
        if user_input.lower() == 'exit':
            print("Exiting program...")
            break
        
        command = process_command_with_openai(user_input)
        
        if command != "unknown":
            # Send the command to the Pico
            ser.write(f"{command}\n".encode())
            print(f"Sent '{command}' command to Pico")
            
            # Read the response from the Pico
            response = ser.readline().decode('utf-8').strip()
            print(f"Pico response: {response}")
        else:
            print("Command not recognized. Try again.")

    # Close the serial connection
    ser.close()

if __name__ == "__main__":
    main()