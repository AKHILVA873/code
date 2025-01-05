import tkinter as tk
from tkinter import ttk
import serial
import time
import threading
import atexit
from shared_memory.shared_memory_util import write_data_to_shared_memory, read_data_from_shared_memory, modify_shared_memory_data

# Global variables for sensor data
water_voltage = None
tacco_value = None
doors_value = None

def send_command_to_relay_controller(command):
    ser_relay.write((command + '\n').encode())
    print(f"Sent to relay controller: {command}")
    time.sleep(2)  # Wait a bit for the command to be processed

def send_command_to_rpm_controller(command):
    ser_rpm.write((command + '\n').encode())
    print(f"Sent to rpm controller: {command}")
    time.sleep(2)  # Wait a bit for the command to be processed

def print_sensor_data(water, tacco, doors):
    water_voltage.set(f"Water Sensor Voltage: {water:.3f} V")
    tacco_value.set(f"Tacco Sensor Value: {tacco}")
    doors_value.set(f"Doors Sensor Value: {doors}")

def read_sensor_data():
    global water_voltage, tacco_value, doors_value
    try:
        while True:
            if ser_sensor.in_waiting > 0:
                line = ser_sensor.readline().decode('utf-8').rstrip()
                
                # Check if the line contains the expected separator
                if ': ' in line:
                    try:
                        sensor_name, value_str = line.split(': ')
                        
                        # Update the sensor data
                        if sensor_name == "watersensor":
                            water_voltage_val = float(value_str)
                            modify_shared_memory_data("watersensor", int(water_voltage_val * 100))
                            water_voltage = water_voltage_val
                        elif sensor_name == "taccosensor":
                            tacco_value_val = int(value_str) * 30
                            modify_shared_memory_data("taccosensor", tacco_value_val)
                            tacco_value = tacco_value_val
                        elif sensor_name == "doorssensor":
                            doors_value_val = int(value_str)
                            modify_shared_memory_data("doorssensor", doors_value_val)
                            doors_value = doors_value_val
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
    ser_sensor.close()

def cleanup_shared_memory(shm):
    def cleanup():
        print("Cleaning up shared memory.")
        shm.close()
        shm.unlink()
    return cleanup

def start_sensor_reading():
    # Start reading sensor data in a separate thread
    sensor_thread = threading.Thread(target=read_sensor_data)
    sensor_thread.daemon = True  # Daemonize thread to close with main program
    sensor_thread.start()

def handle_command(command):
    if command.lower() == 'exit':
        root.quit()
    elif command.isdigit():
        send_command_to_rpm_controller(command)
    else:
        send_command_to_relay_controller(command)

def create_command_button(frame, text):
    button = ttk.Button(frame, text=text, command=lambda: handle_command(text))
    button.pack(pady=5, padx=10, fill=tk.X, anchor=tk.W)
    return button

def initialize_gui():
    # Configure the serial connections to the Arduino
    global ser_relay, ser_rpm, ser_sensor
    
    ser_relay = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Replace with your actual port for relay controller
    time.sleep(2)  # Allow time for the connection to establish
    ser_rpm = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)  # Replace with your actual port for RPM controller
    time.sleep(2)  # Allow time for the connection to establish
    ser_sensor = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Replace with your actual port for sensor data
    time.sleep(2)  # Allow time for the connection to establish
    
    # Initialize tkinter GUI
    root = tk.Tk()
    root.title("Command Sender and Sensor Monitor")

    # Create frames for left (commands) and right (sensor data) sections
    left_frame = ttk.Frame(root)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N)

    right_frame = ttk.Frame(root)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N)

    # Create labels to display sensor data in the right frame
    global water_voltage, tacco_value, doors_value
    water_voltage = tk.DoubleVar()
    tacco_value = tk.IntVar()
    doors_value = tk.IntVar()

    ttk.Label(right_frame, textvariable=water_voltage).pack(pady=5, anchor=tk.W)
    ttk.Label(right_frame, textvariable=tacco_value).pack(pady=5, anchor=tk.W)
    ttk.Label(right_frame, textvariable=doors_value).pack(pady=5, anchor=tk.W)

    # Start sensor reading in a separate thread
    start_sensor_reading()

    # Create buttons in the left frame
    commands = ['st', 'cl', 'ch', 'ah', 'al', 'inlet2H', 'inlet2L', 'inlet1H', 'inlet1L', 'drainH', 'drainL', 'doorH', 'doorL', 'exit']

    for command in commands:
        create_command_button(left_frame, command)

    # Ensure shared memory cleanup on exit
    shm1 = write_data_to_shared_memory("watersensor", 0)
    shm2 = write_data_to_shared_memory("taccosensor", 0)
    shm3 = write_data_to_shared_memory("doorssensor", 0)

    atexit.register(cleanup_shared_memory(shm1))
    atexit.register(cleanup_shared_memory(shm2))
    atexit.register(cleanup_shared_memory(shm3))

    # Start the tkinter main loop
    root.mainloop()

    # Clean up
    ser_relay.close()
    ser_rpm.close()

if __name__ == "__main__":
    initialize_gui()
