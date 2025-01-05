import RPi.GPIO as GPIO
import time
from shared_memory_util import write_data_to_shared_memory

# Define GPIO pins
PWM_PIN = 18  # GPIO 18 for the water level sensor
door_status = 12  # GPIO 12 for the door status

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.IN)
GPIO.setup(door_status, GPIO.IN)  # Setup door status pin as input

def pulse_in(pin, level, timeout=1.0):
    start_time = time.time()
    while GPIO.input(pin) != level:
        if time.time() - start_time > timeout:
            return 0
    start_time = time.time()
    while GPIO.input(pin) == level:
        if time.time() - start_time > timeout:
            return 0
    return (time.time() - start_time) * 1_000_000  # Return duration in microseconds

def read_pwm_frequency():
    high_duration = pulse_in(PWM_PIN, GPIO.HIGH)
    low_duration = pulse_in(PWM_PIN, GPIO.LOW)
    
    if high_duration == 0 or low_duration == 0:
        return 0  # Return 0 if the pulse duration is not measured correctly
    
    period = high_duration + low_duration
    frequency = 1_000_000.0 / period  # Frequency in Hz
    return frequency

if __name__ == "__main__":
    try:
        while True:
            # Read water level sensor PWM frequency
            frequency = read_pwm_frequency()
            write_data_to_shared_memory("Pressure", frequency)
            print(f"Pressure: {frequency:.2f} Hz")

            # Example conversion of frequency to water level (adjust based on calibration)
            water_level_value = frequency * 0.1  # Example conversion factor, adjust as needed
            write_data_to_shared_memory("Water_Level", water_level_value)
            print(f"Water Level: {water_level_value:.2f} units")

            # Read door status
            door_status_value = GPIO.input(door_status)
            write_data_to_shared_memory("Door_Status", float(door_status_value))
            print(f"Door Status: {'Open' if door_status_value == GPIO.LOW else 'Closed'}")

            time.sleep(0.5)  # Delay between readings
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        GPIO.cleanup()
