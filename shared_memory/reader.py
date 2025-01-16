from shared_memory_util import read_data_from_shared_memory
import time

def read_data():
    # Define the shared memory name to read from
    shm_name = "command_from_server"
    
    # Continuously read data from shared memory (example)
    while True:
        data = read_data_from_shared_memory(shm_name)
        print(f"Read data: {data} from shared memory '{shm_name}'")
        time.sleep(1)  # Simulate periodic reading

if __name__ == "__main__":
    read_data()
