import RPi.GPIO as GPIO
import time
from shared_memory_util import read_data_from_shared_memory

# Define GPIO pins for relays
relayPin0 = 17
relayPin1 = 27
relayPin2 = 22
relayPin3 = 23
inlet2 = 6
inlet1 = 13
drain = 19
door = 5

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin0, GPIO.OUT)
GPIO.setup(relayPin1, GPIO.OUT)
GPIO.setup(relayPin2, GPIO.OUT)
GPIO.setup(relayPin3, GPIO.OUT)
GPIO.setup(inlet2, GPIO.OUT)
GPIO.setup(inlet1, GPIO.OUT)
GPIO.setup(drain, GPIO.OUT)
GPIO.setup(door, GPIO.OUT)

# Ensure the relays are initially off
GPIO.output(relayPin0, GPIO.LOW)
GPIO.output(relayPin1, GPIO.LOW)
GPIO.output(relayPin2, GPIO.LOW)
GPIO.output(relayPin3, GPIO.LOW)
GPIO.output(inlet2, GPIO.HIGH)
GPIO.output(inlet1, GPIO.HIGH)
GPIO.output(drain, GPIO.HIGH)
GPIO.output(door, GPIO.HIGH)

def alCommand():
    print("clockwise High command received")
    GPIO.output(relayPin1, GPIO.LOW)
    GPIO.output(relayPin2, GPIO.LOW)
    GPIO.output(relayPin3, GPIO.LOW)
    GPIO.output(relayPin0, GPIO.HIGH)

def ahCommand():
    print("clockwise Low command received")
    GPIO.output(relayPin1, GPIO.HIGH)
    GPIO.output(relayPin2, GPIO.LOW)
    GPIO.output(relayPin3, GPIO.LOW)
    GPIO.output(relayPin0, GPIO.HIGH)

def clCommand():
    print("Anticlock High command received")
    GPIO.output(relayPin1, GPIO.LOW)
    GPIO.output(relayPin2, GPIO.HIGH)
    GPIO.output(relayPin3, GPIO.HIGH)
    GPIO.output(relayPin0, GPIO.HIGH)

def chCommand():
    print("Anticlock Low command received")
    GPIO.output(relayPin1, GPIO.HIGH)
    GPIO.output(relayPin2, GPIO.HIGH)
    GPIO.output(relayPin3, GPIO.HIGH)
    GPIO.output(relayPin0, GPIO.HIGH)

def stCommand():
    print("stop command received")
    GPIO.output(relayPin0, GPIO.LOW)

def inlet2HCommand():
    print("inlet valve 2 open")
    GPIO.output(inlet2, GPIO.LOW)

def inlet2LCommand():
    print("inlet valve 2 close")
    GPIO.output(inlet2, GPIO.HIGH)

def inlet1HCommand():
    print("inlet valve 1 open")
    GPIO.output(inlet1, GPIO.LOW)

def inlet1LCommand():
    print("inlet valve 1 close")
    GPIO.output(inlet1, GPIO.HIGH)

def drainHCommand():
    print("drain pump on")
    GPIO.output(drain, GPIO.LOW)

def drainLCommand():
    print("drain pump off")
    GPIO.output(drain, GPIO.HIGH)

def doorHCommand():
    print("door open")
    GPIO.output(door, GPIO.LOW)

def doorLCommand():
    print("door closed")
    GPIO.output(door, GPIO.HIGH)

if __name__ == "__main__":
    command_map = {
        1.0: chCommand,
        2.0: clCommand,
        3.0: ahCommand,
        4.0: alCommand,
        5.0: stCommand,
        6.0: inlet2HCommand,
        7.0: inlet2LCommand,
        8.0: inlet1HCommand,
        9.0: inlet1LCommand,
        10.0: drainHCommand,
        11.0: drainLCommand,
        12.0: doorHCommand,
        13.0: doorLCommand
    }

    try:
        while True:
            command_value = read_data_from_shared_memory("relay_command")
            command = command_map.get(command_value, None)
            if command:
                command()
            else:
                print(f"Unknown command value received: {command_value}")

            time.sleep(0.5)  # Adjust delay as needed
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        GPIO.cleanup()
