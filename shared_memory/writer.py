from shared_memory_util import write_data_to_shared_memory
import time

def write_data():
    # Define the shared memory name and data to write
    shm_name = "command_from_server"
    data = 1000.0
    
    # Continuously write data to shared memory (example)
    while True:
        write_data_to_shared_memory(shm_name, data)
        print(f"Written data: {data} to shared memory '{shm_name}'")
        time.sleep(1)  # Simulate periodic writing

if __name__ == "__main__":
    write_data()
