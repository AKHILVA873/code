import pigpio
import time
from shared_memory_util import read_data_from_shared_memory, write_data_to_shared_memory

# Define GPIO pins for relays
relayPin0 = 17
relayPin1 = 27
relayPin2 = 22
relayPin3 = 23
inlet2 = 6
inlet1 = 13
drain = 19
door = 5

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Unable to connect to pigpio daemon")

# Ensure the relays are initially off
pi.write(relayPin0, pigpio.LOW)
pi.write(relayPin1, pigpio.LOW)
pi.write(relayPin2, pigpio.LOW)
pi.write(relayPin3, pigpio.LOW)
pi.write(inlet2, pigpio.LOW)
pi.write(inlet1, pigpio.LOW)
pi.write(drain, pigpio.LOW)
pi.write(door, pigpio.LOW)

def chCommand():
    print("clockwise High command received")
    pi.write(relayPin1, pigpio.LOW)
    pi.write(relayPin2, pigpio.LOW)
    pi.write(relayPin3, pigpio.LOW)
    pi.write(relayPin0, pigpio.HIGH)

def clCommand():
    print("clockwise Low command received")
    pi.write(relayPin1, pigpio.HIGH)
    pi.write(relayPin2, pigpio.LOW)
    pi.write(relayPin3, pigpio.LOW)
    pi.write(relayPin0, pigpio.HIGH)

def ahCommand():
    print("Anticlock High command received")
    pi.write(relayPin1, pigpio.LOW)
    pi.write(relayPin2, pigpio.HIGH)
    pi.write(relayPin3, pigpio.HIGH)
    pi.write(relayPin0, pigpio.HIGH)

def alCommand():
    print("Anticlock Low command received")
    pi.write(relayPin1, pigpio.HIGH)
    pi.write(relayPin2, pigpio.HIGH)
    pi.write(relayPin3, pigpio.HIGH)
    pi.write(relayPin0, pigpio.HIGH)

def stCommand():
    print("stop command received")
    pi.write(relayPin0, pigpio.LOW)

def inlet2HCommand():
    print("inlet valve 2 open")
    pi.write(inlet2, pigpio.HIGH)

def inlet2LCommand():
    print("inlet valve 2 close")
    pi.write(inlet2, pigpio.LOW)

def inlet1HCommand():
    print("inlet valve 1 open")
    pi.write(inlet1, pigpio.HIGH)

def inlet1LCommand():
    print("inlet valve 1 close")
    pi.write(inlet1, pigpio.LOW)

def drainHCommand():
    print("drain pump on")
    pi.write(drain, pigpio.HIGH)

def drainLCommand():
    print("drain pump off")
    pi.write(drain, pigpio.LOW)

def doorHCommand():
    print("door pulse activated")
    pi.write(door, pigpio.HIGH)
    time.sleep(0.1)
    pi.write(door, pigpio.LOW)
    write_data_to_shared_memory("relay_command", float(13.0))

def doorLCommand():
    print("door closed")
    pi.write(door, pigpio.LOW)

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
        pi.stop()
