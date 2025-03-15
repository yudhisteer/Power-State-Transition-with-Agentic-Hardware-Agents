# Power-State-Transition-with-Agentic-Hardware-Agents

Note: Pico only run the main.py file.


## References
1. https://www.instructables.com/Control-Your-Arduino-With-Pythons-Pyfirmata-Librar/


# Sensai Project Structure

# Sensai Project Structure

📦 Sensai
├── 📂 src/
│   └── 📂 sensai/                    # Main package
│       ├── 📂 pi/                    # Raspberry Pi components
│       │   ├── 📂 client/            # Pi client implementation
│       │   │   ├── 📄 ds18b20_client.py  # Temperature sensor client
│       │   │   ├── 📄 servo_client.py    # Servo control client
│       │   │   └── 📄 __init__.py
│       │   │
│       │   ├── 📂 server/            # Pi server implementation
│       │   │   ├── 📄 ds18b20_server.py  # Temperature sensor server
│       │   │   ├── 📄 servo_server.py    # Servo control server
│       │   │   └── 📄 __init__.py
│       │
│       ├── 📂 pico/                  # Raspberry Pico components
│       │   ├── 📂 client/            # Pico client implementation
│       │   │   ├── 📄 servo_client.py    # Servo control client
│       │   │   ├── 📄 blink_client.py    # LED control client
│       │   │   └── 📄 __init__.py
│       │   │
│       │   ├── 📂 server/            # Pico server implementation
│       │   │   ├── 📄 servo_server.py    # Servo control server
│       │   │   ├── 📄 blink_server.py    # LED control server
│       │   │   └── 📄 __init__.py
│       │
│       ├── 📂 basics/                # Basic components
│       │   ├── 📄 ds18b20.py        # Temperature sensor implementation
│       │   ├── 📄 servo.py          # Servo motor control
│       │   ├── 📄 blink.py          # LED blinking functionality
│       │   └── 📄 __init__.py
│       │
│       ├── 📂 db/                    # Database related code
│       │   ├── 📄 schemas.py         # Database schemas
│       │   ├── 📄 table_creator.py   # Database table creation
│       │   ├── 📄 supabase_client.py # Supabase client implementation
│       │   └── 📄 __init__.py
│       │
│       └── 📄 __init__.py
│
├── 📂 util/                          # Utility functions
│   ├── 📄 logger_setup.py           # Logging configuration
│   └── 📄 __init__.py
│
├── 📂 .venv/                        # Python virtual environment
├── 📄 setup.py                     # Python package setup configuration
├── 📄 requirements.txt             # Project dependencies
├── 📄 README.md                    # Project documentation
├── 📄 .env                         # Environment variables
├── 📄 .env.example                 # Example environment variables
└── 📄 .gitignore                   # Git ignore rules



# Sensai Project Structure

📦 Sensai
├── 📂 src/
│   └── 📂 sensai/           # Main package
│       ├── 📂 pi/           # Raspberry Pi components
│       │   ├── 📂 client/   # Pi client implementation
│       │   └── 📂 server/   # Pi server implementation
│       │
│       ├── 📂 pico/         # Raspberry Pico components
│       │   ├── 📂 client/   # Pico client implementation
│       │   └── 📂 server/   # Pico server implementation
│       │
│       ├── 📂 basics/       # Basic components
│       │   ├── 📄 ds18b20.py    # Temperature sensor implementation
│       │   ├── 📄 servo.py      # Servo motor control
│       │   ├── 📄 blink.py      # LED blinking functionality
│       │   └── 📄 __init__.py
│       │
│       ├── 📂 db/           # Database related code
│       └── 📄 __init__.py   # Package initializer
│
├── 📂 util/                 # Utility functions
│   ├── 📄 logger_setup.py   # Logging configuration
│   └── 📄 __init__.py
│
├── 📂 .venv/               # Python virtual environment
├── 📄 setup.py            # Python package setup configuration
├── 📄 requirements.txt    # Project dependencies
├── 📄 README.md          # Project documentation
├── 📄 .env               # Environment variables
├── 📄 .env.example       # Example environment variables
└── 📄 .gitignore        # Git ignore rules