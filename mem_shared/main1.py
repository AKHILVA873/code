from shared_memory_util import create_shared_memory, write_data_to_shared_memory

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
    "doorL": 13.0
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
    "command_from_server"
        # Added for TRIAC delay
]

def initialize_shared_memory():
    for name in shared_memory_names:
        create_shared_memory(name, 4)  # Initialize all shared memories with size 4 (float)

if __name__ == "_main_":
    # Initialize all shared memory segments
    initialize_shared_memory()

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
                write_data_to_shared_memory("relay_command", command_to_float[user_input])
                print(f"Command '{user_input}' written to shared memory.")
            else:
                print("Unknown command.")
