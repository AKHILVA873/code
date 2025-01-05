import RPi.GPIO as GPIO
import time
import threading
from shared_memory_util import read_data_from_shared_memory

# GPIO pins
TRIAC_PIN = 24
INPUT_PIN = 25

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIAC_PIN, GPIO.OUT)
GPIO.setup(INPUT_PIN, GPIO.IN)

# Global variable to store the TRIAC delay
triac_delay = 8000  # Default value in microseconds
triac_delay_lock = threading.Lock()
triac_delay_updated = threading.Event()

def triac_control():
    while True:
        sensor_value = GPIO.input(INPUT_PIN)
        if sensor_value == GPIO.HIGH:
            GPIO.output(TRIAC_PIN, GPIO.LOW)
            with triac_delay_lock:
                delay = triac_delay
            time.sleep(delay / 1_000_000)  # Convert microseconds to seconds
            GPIO.output(TRIAC_PIN, GPIO.HIGH)


def monitor_triac_delay():
    global triac_delay
    while True:
        # Read the triac delay value from shared memory
        new_triac_delay = read_data_from_shared_memory("triac_delay")
        with triac_delay_lock:
            if triac_delay != new_triac_delay:
                triac_delay = new_triac_delay
                print(f"Updated TRIAC delay: {triac_delay}")
                triac_delay_updated.set()
        time.sleep(0.1)  # Adjust the delay as needed

if __name__ == "__main__":
    try:
        # Create and start the TRIAC control thread
        triac_thread = threading.Thread(target=triac_control)
        triac_thread.start()

        # Create and start the monitor TRIAC delay thread
        monitor_thread = threading.Thread(target=monitor_triac_delay)
        monitor_thread.start()

        # Wait for threads to complete (this will actually run indefinitely)
        triac_thread.join()
        monitor_thread.join()

    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        GPIO.cleanup()
