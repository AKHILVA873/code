import RPi.GPIO as GPIO
import time

# Define GPIO pin numbers
TRIAC_PULSE = 10
INPUT_PIN = 2
delay_value = 7000  # Default delay value in microseconds

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIAC_PULSE, GPIO.OUT)  # Set the TRIAC_PULSE pin as output
GPIO.setup(INPUT_PIN, GPIO.IN)     # Set the INPUT_PIN to read sensor values

print("Enter delay value in microseconds:")

def get_input_value():
    try:
        return int(input())
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return get_input_value()

try:
    while True:
        # Check if there's serial input (simulated with standard input here)
        if GPIO.input(INPUT_PIN) == GPIO.HIGH:
            GPIO.output(TRIAC_PULSE, GPIO.LOW)   # Set the TRIAC_PULSE pin LOW
            time.sleep(delay_value / 1000000.0)  # Wait for the specified microseconds
            GPIO.output(TRIAC_PULSE, GPIO.HIGH)
        
        # Read and update delay value from user
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            delay_value = get_input_value()
            print(f"New delay value set to: {delay_value}")
finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit
