import serial
import time

# Configure the serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Replace '/dev/ttyACM0' with your port if different
time.sleep(2)  # Wait for the connection to establish

# Continuously read data from the serial port
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
except KeyboardInterrupt:
    print("Program terminated by user")

# Close the serial connection
ser.close()

