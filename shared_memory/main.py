from shared_memory_util import create_shared_memory, write_data_to_shared_memory
import os
import sys
import time

# Command to float value mapping
command_to_float = {
    "ch": 1.0,
    "cl": 2.0,
    "ah": 3.0,
    "al": 4.0,
    "st": 5.0,
    "inlet2H": 6.0,
    "inlet2L": 7.0,
    "inlet1H": 8.0,
    "inlet1L": 9.0,
    "drainH": 10.0,
    "drainL": 11.0,
    "doorH": 12.0,
    "doorL": 13.0,
}

# Shared memory names
shared_memory_names = [
    "relay_command",
    "taccosensor",
    "doorssensor",
    "Pressure",
    "Water_Level",
    "Door_Status",
    "triac_delay",
    "command_from_server",  # For TRIAC delay
]

def initialize_shared_memory():
    """
    Create and initialize shared memory segments for the given names.
    Each shared memory segment is initialized with a size of 4 (float).
    """
    for name in shared_memory_names:
        try:
            create_shared_memory(name, 4)
            print(f"Shared memory '{name}' initialized.")
        except Exception as e:
            print(f"Failed to initialize shared memory '{name}': {e}")
    write_data_to_shared_memory("command_from_server", 1000.0)


def interactive_mode():
    """Run the script in interactive mode."""
    while True:
        user_input = input("Enter command or TRIAC delay (number): ").strip()
        try:
            # Check if the input is a number
            triac_delay = float(user_input)
            write_data_to_shared_memory("triac_delay", triac_delay)
            print(f"TRIAC delay '{triac_delay}' written to shared memory.")
        except ValueError:
            # If it's not a number, check if it's a command
            if user_input in command_to_float:
                try:
                    command_value = command_to_float[user_input]
                    write_data_to_shared_memory("relay_command", command_value)
                    print(f"Command '{user_input}' written to shared memory.")
                except Exception as e:
                    print(f"Failed to write command '{user_input}' to shared memory: {e}")
            else:
                print("Unknown command.")

def service_mode():
    """Run the script in non-interactive mode."""
    print("Running in service mode...")
    while True:
        # Placeholder for non-interactive logic
        # Replace with your desired behavior
        print("Service mode is active. Waiting for external inputs...")
        time.sleep(10)

if __name__ == "__main__":
    # Initialize all shared memory segments
    initialize_shared_memory()

    # Check if running interactively or as a service
    if os.isatty(sys.stdin.fileno()):
        interactive_mode()
    else:
        service_mode()
    
