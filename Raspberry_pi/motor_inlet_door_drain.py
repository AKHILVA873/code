import RPi.GPIO as GPIO

# Define the GPIO pins connected to the relays
relayPin0 = 17
relayPin1 = 27
relayPin2 = 22
relayPin3 = 23

door = 5
inlet2 = 6
inlet1 = 13
drain = 19

# Function prototypes
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

# Set up the GPIO pins
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

# Main loop
try:
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
        else:
            print("Unknown command")

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()
