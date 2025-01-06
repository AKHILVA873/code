from shared_memory_util import modify_shared_memory_data
import time

if __name__ == "__main__":
    shared_memory_name = "demo_shared_memory_single_float"

    # Modify float data in shared memory
    new_data = 10.123  # Example new data to write
    modify_shared_memory_data(shared_memory_name, new_data)
    print(f"Modified data in shared memory to {new_data:.3f}.")

    while True:
        time.sleep(1)  # Keeping the process alive to demonstrate the modification
