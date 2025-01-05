import RPi.GPIO as GPIO
import time

# Constants
ZERO_CROSS_PIN = 20  # Change to another GPIO pin
INTERVAL = 1  # Measurement interval in seconds

# Variables
zero_cross_count = 0
previous_time = time.time()

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ZERO_CROSS_PIN, GPIO.IN)

def zero_cross_callback(channel):
    global zero_cross_count
    zero_cross_count += 1

# Try to attach the interrupt to the zero-crossing pin
try:
    GPIO.add_event_detect(ZERO_CROSS_PIN, GPIO.RISING, callback=zero_cross_callback)
except RuntimeError as e:
    print(f"Error: {e}")
    GPIO.cleanup()
    exit(1)

try:
    while True:
        current_time = time.time()
        if current_time - previous_time >= INTERVAL:
            # Disable interrupts temporarily
            GPIO.remove_event_detect(ZERO_CROSS_PIN)
            zero_crosses = zero_cross_count
            zero_cross_count = 0
            GPIO.add_event_detect(ZERO_CROSS_PIN, GPIO.RISING, callback=zero_cross_callback)

            # Calculate cycles and frequency
            cycles = zero_crosses / 3.0  # Calculate the number of cycles
            frequency = cycles / INTERVAL  # Cycles per second
            rpm = (frequency / 3.0) * 60.0  # Convert frequency to RPM
            rpm_div_10 = rpm / 10.0  # Divide RPM by 10 for display

            # Print RPM with one decimal place
            print(f"RPM: {rpm_div_10:.1f}")

            previous_time = current_time

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
finally:
    GPIO.cleanup()

