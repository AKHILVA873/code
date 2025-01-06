import RPi.GPIO as GPIO
import time
import smbus
from shared_memory_util import write_data_to_shared_memory

# Define GPIO pins
DIGITAL_PIN = 4  # GPIO 4 for the digital input
PWM_PIN = 18  # GPIO 18 for the water level sensor
door_status = 12  # GPIO 12 for the door status

# I2C setup for PCF8591
bus = smbus.SMBus(1)
PCF8591_ADDRESS = 0x48

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIGITAL_PIN, GPIO.IN)
GPIO.setup(PWM_PIN, GPIO.IN)
GPIO.setup(door_status, GPIO.IN)  # Setup door status pin as input

def read_pcf8591(channel):
    if channel < 0 or channel > 3:
        raise ValueError('Channel must be between 0 and 3')
    bus.write_byte(PCF8591_ADDRESS, 0x40 | channel)
    value = bus.read_byte(PCF8591_ADDRESS)  # Dummy read to start conversion
    value = bus.read_byte(PCF8591_ADDRESS)
    return value

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
            # Read analog value from PCF8591
            analog_value = read_pcf8591(0)
            write_data_to_shared_memory("taccosensor", float(analog_value))
            print(f"taccosensor: {analog_value}")

            # Read digital pin value
            digital_value = GPIO.input(DIGITAL_PIN)
            write_data_to_shared_memory("doorssensor", float(digital_value))
            print(f"doorssensor: {digital_value}")

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
            print(f"Door Status: {'Open' if door_status_value == GPIO.HIGH else 'Closed'}")

            time.sleep(0.5)  # Delay between readings
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        GPIO.cleanup()
