import requests
import time
from shared_memory_util import create_shared_memory, write_data_to_shared_memory

# Define the URL of the API
API_URL = 'http://localhost:3000/command_to_machine'

def fetch_command():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def main():
    while True:
        data = fetch_command()
        if data and 'command' in data:
            if data['command'] == 'start':
                print("Start command received from the cloud")
                cmd = 1.0
                write_data_to_shared_memory("command_from_server", cmd)
            else:
                print("Waiting for the start command")
        else:
            print("Invalid response or no command found")

        time.sleep(5)  # Wait for 5 seconds before fetching the data again

if _name_ == '_main_':
    main()
