import time
from shared_memory_util import write_data_to_shared_memory

try:
    while True:
        rpm = input("Enter the RPM: ")
        # Convert the input to a number (int or float depending on the requirement)
        rpm = float(rpm)  # Use int() if you expect integer RPM values
        write_data_to_shared_memory("taccosensor", rpm)
        time.sleep(1)  # Measurement interval of 1 second

except KeyboardInterrupt:
    print("Measurement stopped by user")
