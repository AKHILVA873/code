import tkinter as tk
from tkinter import ttk
import serial
import time
import threading

# Initialize Arduino serial connections
ser1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Arduino on ACM0
ser2 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Arduino on USB0
ser3 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)  # Arduino on USB1

time.sleep(2)  # Wait for the connections to establish

# Initialize sensor variables
water_voltage = None
tacco_value = None
doors_value = None

def send_command_to_relay_controller(ser, command):
    ser2.write((command + '\n').encode())
    print(f"Sent to relay controller on {ser.name}: {command}")
    # time.sleep(2)  # Wait a bit for the command to be processed

def send_command_to_rpm_controller(ser, command):
    ser3.write((command + '\n').encode())
    print(f"Sent to rpm controller on {ser.name}: {command}")
    # time.sleep(2)  # Wait a bit for the command to be processed

def handle_command(command):
    if command.lower() == 'exit':
        root.quit()
    elif command.isdigit():
        send_command_to_rpm_controller(ser3, command)  # Example usage with ser1 (adjust as needed)
    else:
        send_command_to_relay_controller(ser2, command)  # Example usage with ser1 (adjust as needed)

def read_sensor_data(ser):
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
                        elif sensor_name == "taccosensor":
                            tacco_value = int(value_str) * 30
                        elif sensor_name == "doorssensor":
                            doors_value = int(value_str)
                        else:
                            print(f"Unknown sensor: {sensor_name}")
                        
                        # Update GUI with the latest sensor data
                        update_sensor_data()

                    except ValueError as e:
                        print(f"Error processing line '{line}': {e}")
                else:
                    print(f"Malformed line: {line}")

    except KeyboardInterrupt:
        print("Program terminated by user")

    # Close the serial connection
    ser.close()

def update_sensor_data():
    # Update GUI elements with the latest sensor data
    if water_voltage is not None:
        water_sensor_label.config(text=f"Water Voltage: {water_voltage:.2f} V")
    if tacco_value is not None:
        tacco_sensor_label.config(text=f"Tacco Value: {tacco_value}")
    if doors_value is not None:
        doors_sensor_label.config(text=f"Doors Value: {doors_value}")

# GUI setup
root = tk.Tk()
root.title("Command Sender and Sensor Display")

# Divide the GUI into 4 parts using LabelFrames
frame1 = ttk.LabelFrame(root, text='Direction')
frame1.grid(row=0, column=0, padx=15, pady=15, sticky=tk.W+tk.E+tk.N+tk.S)

frame2 = ttk.LabelFrame(root, text='Water Inlet')
frame2.grid(row=0, column=1, padx=15, pady=15, sticky=tk.W+tk.E+tk.N+tk.S)

frame3 = ttk.LabelFrame(root, text='Water Drain')
frame3.grid(row=1, column=0, padx=15, pady=15, sticky=tk.W+tk.E+tk.N+tk.S)

frame4 = ttk.LabelFrame(root, text='Door')
frame4.grid(row=1, column=1, padx=15, pady=15, sticky=tk.W+tk.E+tk.N+tk.S)

# Function to create buttons for each command within a specific frame
def create_command_button(frame, text):
    button = ttk.Button(frame, text=text, command=lambda: handle_command(text))
    button.pack(pady=5, padx=10, fill=tk.X)
    return button

# Commands to create buttons for
commands = ['st', 'cl', 'ch', 'ah', 'al', 'inlet2H', 'inlet2L', 'inlet1H', 'inlet1L', 'drainH', 'drainL', 'doorH', 'doorL', 'exit']

# Create buttons for each command in each frame
for i, command in enumerate(commands):
    if i < 5:
        create_command_button(frame1, command)
    elif i < 9:
        create_command_button(frame2, command)
    elif i < 11:
        create_command_button(frame3, command)
    else:
        create_command_button(frame4, command)

# RPM input and send button
rpm_label = ttk.Label(root, text="Enter RPM:")
rpm_label.grid(row=2, column=0, columnspan=2, pady=10)

rpm_entry = ttk.Entry(root, width=30)
rpm_entry.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

def send_rpm_command():
    rpm_value = rpm_entry.get()
    if rpm_value.isdigit():
        send_command_to_rpm_controller(ser3, rpm_value)  # Example usage with ser1 (adjust as needed)

rpm_button = ttk.Button(root, text="Send RPM", command=send_rpm_command)
rpm_button.grid(row=4, column=0, columnspan=2, pady=10)

# Sensor data display labels
sensor_data_frame = ttk.LabelFrame(root, text='Sensor Data')
sensor_data_frame.grid(row=0, column=2, rowspan=2, padx=15, pady=15, sticky=tk.W+tk.E+tk.N+tk.S)

water_sensor_label = ttk.Label(sensor_data_frame, text="Water Voltage: ")
water_sensor_label.pack(pady=5)

tacco_sensor_label = ttk.Label(sensor_data_frame, text="Tacco Value: ")
tacco_sensor_label.pack(pady=5)

doors_sensor_label = ttk.Label(sensor_data_frame, text="Doors Value: ")
doors_sensor_label.pack(pady=5)

# Start threads to read and update sensor data for each Arduino
sensor_threads = []
for ser in [ser1]:
    sensor_thread = threading.Thread(target=read_sensor_data, args=(ser,))
    sensor_thread.daemon = True  # Daemonize thread so it stops with the main program
    sensor_thread.start()
    sensor_threads.append(sensor_thread)

root.mainloop()

# Clean up
ser1.close()
ser2.close()
ser3.close()
