import serial
import time
import atexit
# from shared_memory.shared_memory_util import write_data_to_shared_memory, read_data_from_shared_memory, modify_shared_memory_data

# Configure the serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Replace '/dev/ttyACM0' with your port if different
time.sleep(2)  # Wait for the connection to establish

# Initialize sensor variables
water_voltage = None
tacco_value = None
doors_value = None

def print_sensor_data(water, tacco, doors):
    print(f"Water Sensor Voltage: {water:.3f} V, Tacco Sensor Analog Value: {tacco}, Doors Sensor Digital Value: {doors}")

def read_data():
    global water_voltage, tacco_value, doors_value
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                
                # Check if the line contains the expected separator
                if ': ' in line:
                    try:
                        sensor_name, value_str = line.split(': ')
                        
                        # Update the sensor data
                        if sensor_name == "watersensor":
                            water_voltage = float(value_str)
                            # modify_shared_memory_data("watersensor", int(water_voltage * 100))
                        elif sensor_name == "taccosensor":
                            tacco_value = int(value_str)*30
                            # modify_shared_memory_data("taccosensor", tacco_value)
                        elif sensor_name == "doorssensor":
                            doors_value = int(value_str)
                            # modify_shared_memory_data("doorssensor", doors_value)
                        else:
                            print(f"Unknown sensor: {sensor_name}")
                        
                        # Print the data if all sensors have been updated at least once
                        if water_voltage is not None and tacco_value is not None and doors_value is not None:
                            print_sensor_data(water_voltage, tacco_value, doors_value)
                            
                    except ValueError as e:
                        print(f"Error processing line '{line}': {e}")
                else:
                    print(f"Malformed line: {line}")

    except KeyboardInterrupt:
        print("Program terminated by user")

    # Close the serial connection
    ser.close()

# def cleanup_shared_memory(shm):
#     def cleanup():
#         print("Cleaning up shared memory.")
#         shm.close()
#         shm.unlink()
#     return cleanup

if __name__ == "__main__":
    # shm1 = write_data_to_shared_memory("watersensor", 0)
    # shm2 = write_data_to_shared_memory("taccosensor", 0)
    # shm3 = write_data_to_shared_memory("doorssensor", 0)

    # atexit.register(cleanup_shared_memory(shm1))
    # atexit.register(cleanup_shared_memory(shm2))
    # atexit.register(cleanup_shared_memory(shm3))
    

    read_data()
