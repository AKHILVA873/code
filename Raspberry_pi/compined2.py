import RPi.GPIO as GPIO
import time
import threading

# Define GPIO pins
relayPin0 = 17
relayPin1 = 27
relayPin2 = 22
relayPin3 = 23
door = 5
inlet2 = 6
inlet1 = 13
drain = 19
triacPulse = 10
inputPin = 2

# Default delay value
delayValue = 7000
delay_lock = threading.Lock()

# Function prototypes for relay control
def chCommand():
    print("clockwise High command received")
    GPIO.output(relayPin1, GPIO.LOW)
    GPIO.output(relayPin2, GPIO.LOW)
    GPIO.output(relayPin3, GPIO.LOW)
    GPIO.output(relayPin0, GPIO.HIGH)

def clCommand():
    print("clockwise Low command received")
    GPIO.output(relayPin1, GPIO.HIGH)
    GPIO.output(relayPin2, GPIO.LOW)
    GPIO.output(relayPin3, GPIO.LOW)
    GPIO.output(relayPin0, GPIO.HIGH)

def ahCommand():
    print("Anticlock High command received")
    GPIO.output(relayPin1, GPIO.LOW)
    GPIO.output(relayPin2, GPIO.HIGH)
    GPIO.output(relayPin3, GPIO.HIGH)
    GPIO.output(relayPin0, GPIO.HIGH)

def alCommand():
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

# Set up the GPIO pins for relay control
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin0, GPIO.OUT)
GPIO.setup(relayPin1, GPIO.OUT)
GPIO.setup(relayPin2, GPIO.OUT)
GPIO.setup(relayPin3, GPIO.OUT)
GPIO.setup(door, GPIO.OUT)
GPIO.setup(inlet2, GPIO.OUT)
GPIO.setup(inlet1, GPIO.OUT)
GPIO.setup(drain, GPIO.OUT)

# Ensure the relays are initially off
GPIO.output(relayPin0, GPIO.LOW)
GPIO.output(relayPin1, GPIO.LOW)
GPIO.output(relayPin2, GPIO.LOW)
GPIO.output(relayPin3, GPIO.LOW)
GPIO.output(door, GPIO.HIGH)
GPIO.output(inlet2, GPIO.HIGH)
GPIO.output(inlet1, GPIO.HIGH)
GPIO.output(drain, GPIO.HIGH)

# Set up the GPIO pins for triac control
GPIO.setup(triacPulse, GPIO.OUT)
GPIO.setup(inputPin, GPIO.IN)

# Function to handle triac control
def triac_control():
    global delayValue
    while True:
        sensorValue = GPIO.input(inputPin)
        if sensorValue == GPIO.HIGH:
            GPIO.output(triacPulse, GPIO.LOW)
            with delay_lock:
                delay = delayValue
            time.sleep(delay / 1_000_000)  # Convert microseconds to seconds
            GPIO.output(triacPulse, GPIO.HIGH)
        time.sleep(0.01)  # Add a small delay to prevent excessive CPU usage

# Function to handle relay control commands
def relay_control():
    global delayValue
    while True:
        command = input("Enter command: ").strip()
        if command == "ch":
            chCommand()
        elif command == "cl":
            clCommand()
        elif command == "ah":
            ahCommand()
        elif command == "al":
            alCommand()
        elif command == "st":
            stCommand()
        elif command == "inlet2H":
            inlet2HCommand()
        elif command == "inlet2L":
            inlet2LCommand()
        elif command == "inlet1H":
            inlet1HCommand()
        elif command == "inlet1L":
            inlet1LCommand()
        elif command == "drainH":
            drainHCommand()
        elif command == "drainL":
            drainLCommand()
        elif command == "doorH":
            doorHCommand()
        elif command == "doorL":
            doorLCommand()
        elif command.startswith("setDelay"):
            try:
                new_delay = int(command.split()[1])
                with delay_lock:
                    delayValue = new_delay
                print(f"New delay value set to: {delayValue}")
            except ValueError:
                print("Invalid delay value")
        else:
            print("Unknown command")

# Start the relay control and triac control in separate threads
try:
    triac_thread = threading.Thread(target=triac_control)
    relay_thread = threading.Thread(target=relay_control)

    triac_thread.start()
    relay_thread.start()

    triac_thread.join()
    relay_thread.join()

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()
