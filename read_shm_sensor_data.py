import time
from shared_memory.shared_memory_util import read_data_from_shared_memory
global water_voltage
global tacco_value
global doors_value
water_voltage=0
tacco_value=0
tacco_value=0


def read_and_display_shared_memory():
    global water_voltage
    global tacco_value
    global doors_value
    try:
        water_voltage = read_data_from_shared_memory("watersensor")
        tacco_value = read_data_from_shared_memory("taccosensor")
        doors_value = read_data_from_shared_memory("doorssensor")

        # Convert the water voltage back to float
        if water_voltage is not None:
            water_voltage = water_voltage / 100.0

        print(f"Water Sensor Voltage: {water_voltage:.3f} V, Tacco Sensor Analog Value: {tacco_value}, Doors Sensor Digital Value: {doors_value}")

        # Sleep for a while before reading again

    except KeyboardInterrupt:
        print("Program terminated by user")

if __name__ == "__main__":
    read_and_display_shared_memory()
