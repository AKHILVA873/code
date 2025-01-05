import serial
import time

# Configure the serial connection to the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Replace '/dev/ttyUSB0' with your port if different
time.sleep(2)  # Wait for the connection to establish
# ser1 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)  # Replace '/dev/ttyUSB1' with your port if different
# time.sleep(2)  # Wait for the connection to establish

def send_command_to_relay_controller(command):
    ser.write((command + '\n').encode())
    print("sended to relay controller")
    time.sleep(2)  # Wait a bit for the command to be processed

# def send_command_to_rpm_controller(command):
#     ser1.write((command + '\n').encode())
#     print("sended to rpm controller")
#     time.sleep(2)  # Wait a bit for the command to be processed


try:
    while True:
        command = input("Enter command (ch, cl, ah, al, st, inlet2H, inlet2L, inlet1H, inlet1L, drainH, drainL, doorH, doorL, or 'exit' to quit): ")
        if command == 'exit':
            break
        # if command.isdigit():  # Check if the command is a numeric string

        #     send_command_to_rpm_controller(command)
        # else:
        send_command_to_relay_controller(command)
except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    # Close the serial connections
    # ser.close()
    ser1.close()
