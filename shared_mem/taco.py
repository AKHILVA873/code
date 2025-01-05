import pigpio
import time

# Constants
GPIO_PIN = 16  # GPIO pin number (BCM mode)
INTERVAL = 1   # Interval in seconds to calculate RPM

# Global variables
pulse_count = 0
last_time = time.time()

# Initialize pigpio and set up GPIO
pi = pigpio.pi()

if not pi.connected:
    exit()

pi.set_mode(GPIO_PIN, pigpio.INPUT)
pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_UP)

# Define callback function
def count_pulse(gpio, level, tick):
    global pulse_count
    pulse_count += 1

# Attach the callback function to the GPIO pin
pi.callback(GPIO_PIN, pigpio.RISING_EDGE, count_pulse)

try:
    while True:
        current_time = time.time()
        elapsed_time = current_time - last_time
        
        if elapsed_time >= INTERVAL:
            pi.callback(GPIO_PIN).cancel()  # Disable callback during calculation
            
            frequency = (pulse_count * 1000.0) / (elapsed_time * 1000.0)  # Frequency in Hz
            rpm = frequency * 60.0  # Convert Hz to RPM
            
            print(f"Frequency: {frequency:.2f} Hz, RPM: {rpm:.2f}")
            
            pulse_count = 0  # Reset pulse count
            last_time = current_time  # Update last time
            
            pi.callback(GPIO_PIN, pigpio.RISING_EDGE, count_pulse)  # Re-enable callback
            
        time.sleep(0.1)  # Small delay to prevent high CPU usage

except KeyboardInterrupt:
    print("Exiting...")

finally:
    pi.stop()  # Clean up
