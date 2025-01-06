import time
import pigpio

# Initialize pigpio and GPIO
pi = pigpio.pi()
pulse_gpio = 16  # GPIO pin connected to the LM393 output (BCM numbering)

pulse_count = 0
last_time = time.time()

# Callback function to count pulses
def count_pulse(gpio, level, tick):
    global pulse_count
    pulse_count += 1

# Set up the callback for rising edge detection
pi.set_mode(pulse_gpio, pigpio.INPUT)
pi.callback(pulse_gpio, pigpio.RISING_EDGE, count_pulse)

try:
    while True:
        time.sleep(1)  # Measurement interval of 1 second
        current_time = time.time()
        elapsed_time = current_time - last_time
        last_time = current_time

        frequency = pulse_count / elapsed_time  # Frequency in Hz
        rpm = frequency * 60.0  # Convert Hz to RPM

        print(f"Frequency: {frequency:.2f} Hz, RPM: {rpm:.2f}")

        pulse_count = 0  # Reset pulse count

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    pi.stop()  # Clean up and stop pigpio
