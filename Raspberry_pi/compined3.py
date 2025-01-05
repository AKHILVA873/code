import RPi.GPIO as GPIO
import spidev
import time
import threading
from hx711 import HX711

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
DIGITAL_PIN = 4  # GPIO 4 for the digital input
ANALOG_CHANNEL = 0  # MCP3008 channel 0

# Default delay value
delayValue = 7000
delay_lock = threading.Lock()

# HX711 setup
hx = HX711(DOUT_PIN, PD_SCK_PIN)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)
hx.reset()
hx.tare()

# SPI setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Open bus 0, device 0
spi.max_speed_hz = 1350000

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin0, GPIO.OUT)
GPIO.setup(relayPin1, GPIO.OUT)
GPIO.setup(relayPin2, GPIO.OUT)
GPIO.setup(relayPin3, GPIO.OUT)
GPIO.setup(door, GPIO.OUT)
GPIO.setup(inlet2, GPIO.OUT)
GPIO.setup(inlet1, GPIO.OUT)
GPIO.setup(drain, GPIO.OUT)
GPIO.setup(triacPulse, GPIO.OUT)
GPIO.setup(inputPin, GPIO.IN)
GPIO.setup(DIGITAL_PIN, GPIO.IN)

# Ensure the relays are initially off
GPIO.output(relayPin0, GPIO.LOW)
GPIO.output(relayPin1, GPIO.LOW)
GPIO.output(relayPin2, GPIO.LOW)
GPIO.output(relayPin3, GPIO.LOW)
GPIO.output(door, GPIO.HIGH)
GPIO.output(inlet2, GPIO.HIGH)
GPIO.output(inlet1, GPIO.HIGH)
GPIO.output(drain, GPIO.HIGH)

def read_adc(channel):
    if channel < 0 or channel > 7:
        raise ValueError('Channel must be between 0 and 7')
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

def read_hx711():
    return hx.get_weight(5)  # Get the average of 5 readings

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

def sensor_reading():
    while True:
        # Read from HX711
        count = read_hx711()
        voltage = (count / 16777216.0) * 5.0  # Convert count to voltage
        water_level = voltage * 10.0  # Example conversion factor, adjust as needed
        print(f"watersensor: {voltage:.3f}")

        # Read analog value from MCP3008
        analog_value = read_adc(ANALOG_CHANNEL)
        print(f"taccosensor: {analog_value}")

        # Read digital pin value
        digital_value = GPIO.input(DIGITAL_PIN)
        print(f"doorssensor: {digital_value}")

        time.sleep(0.5)  # Delay between readings

# Start the relay control, triac control, and sensor reading in separate threads
try:
    triac_thread = threading.Thread(target=triac_control)
    relay_thread = threading.Thread(target=relay_control)
    sensor_thread = threading.Thread(target=sensor_reading)

    triac_thread.start()
    relay_thread.start()
    sensor_thread.start()

    triac_thread.join()
    relay_thread.join()
    sensor_thread.join()

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()
