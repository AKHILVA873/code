import tkinter as tk
from tkinter import ttk
import serial
import time

# Configure the serial connections to the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Replace '/dev/ttyUSB0' with your port if different
time.sleep(2)  # Wait for the connection to establish
ser1 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)  # Replace '/dev/ttyUSB1' with your port if different
time.sleep(2)  # Wait for the connection to establish

def send_command_to_relay_controller(command):
    ser.write((command + '\n').encode())
    print(f"Sent to relay controller: {command}")
    time.sleep(2)  # Wait a bit for the command to be processed

def send_command_to_rpm_controller(command):
    ser1.write((command + '\n').encode())
    print(f"Sent to rpm controller: {command}")
    time.sleep(2)  # Wait a bit for the command to be processed

def handle_command(command):
    if command.lower() == 'exit':
        root.quit()
    elif command.isdigit():
        send_command_to_rpm_controller(command)
    else:
        send_command_to_relay_controller(command)

# GUI setup
root = tk.Tk()
root.title("Command Sender")

# Divide the GUI into 4 parts using LabelFrames
frame1 = ttk.LabelFrame(root, text='Diraction')
frame1.grid(row=0, column=0, padx=15, pady=15, sticky=tk.W+tk.E+tk.N+tk.S)

frame2 = ttk.LabelFrame(root, text='Water inlet')
frame2.grid(row=0, column=1, padx=15, pady=15, sticky=tk.W+tk.E+tk.N+tk.S)

frame3 = ttk.LabelFrame(root, text='Water drain')
frame3.grid(row=1, column=0, padx=15, pady=15, sticky=tk.W+tk.E+tk.N+tk.S)

frame4 = ttk.LabelFrame(root, text='door')
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
        send_command_to_rpm_controller(rpm_value)

rpm_button = ttk.Button(root, text="Send RPM", command=send_rpm_command)
rpm_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

# Clean up
ser.close()
ser1.close()
