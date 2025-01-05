import serial
import time
from shared_memory.shared_memory_util import read_data_from_shared_memory

# Global variables
command = 7500
required_rpm = 700

ser1 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)  # Adjust port as necessary
time.sleep(2)  # Wait for serial connection


def read_and_display_shared_memory():
    global water_voltage, tacco_value, doors_value
    try:
        water_voltage = read_data_from_shared_memory("watersensor")
        tacco_value = read_data_from_shared_memory("taccosensor")
        doors_value = read_data_from_shared_memory("doorssensor")

        # Convert the water voltage back to float if applicable
        if water_voltage is not None:
            water_voltage = water_voltage / 100.0

        print(f"Water Sensor Voltage: {water_voltage:.3f} V, Tacco Sensor Analog Value: {tacco_value}, Doors Sensor Digital Value: {doors_value}")

    except KeyboardInterrupt:
        print("Program terminated by user")


def send_command_to_rpm_controller(command):
    try:
        ser1.write((str(command) + '\n').encode())  # Ensure command is converted to string
        print(f"Sent command {command} to RPM controller")
        # time.sleep(2)  # Wait for command to be processed

    except Exception as e:
        print(f"Error sending command: {e}")

def rpm_controll():
    global command
    try:
        while True:
            tacco_value = read_data_from_shared_memory("taccosensor")

            if tacco_value > required_rpm:
                command += 40
                if command >8000:
                    command=7000
                send_command_to_rpm_controller(command)

            elif tacco_value < required_rpm:
                command -= 40
                if command <5000:
                    command=6000
                send_command_to_rpm_controller(command)

            else:
                print("In the control range")

            time.sleep(0.2)  # Adjust as necessary to avoid excessive reads

    except KeyboardInterrupt:
        print("Program terminated by user")

    finally:
        ser1.close()  # Close the serial connection


if __name__ == "__main__":
    rpm_controll()
