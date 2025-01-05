from controller_basement import (
    chCommand, clCommand, ahCommand, alCommand, stCommand,
    inlet2HCommand, inlet2LCommand, inlet1HCommand, inlet1LCommand,
    drainHCommand, drainLCommand, doorHCommand, doorLCommand, setup_gpio, cleanup_gpio, start_threads
)
import time

if __name__ == "__main__":
    try:
        # Initialize GPIO
        setup_gpio()

        # Specify a custom delay value (in microseconds)
        custom_delay_value = 5000  # Example delay value

        # Start threads with custom delay value
        triac_thread, relay_thread, sensor_thread = start_threads(delayValue=custom_delay_value)

        # Example usage of commands
        print("Executing commands:")
        chCommand()
        time.sleep(1)
        stCommand()
        time.sleep(30)
        ahCommand()
        time.sleep(1)
        stCommand()
        time.sleep(30)
        alCommand()
        time.sleep(1)
        stCommand()
        time.sleep(30)


        # Example of updating delay value dynamically
        print("Updating delay value...")
        # Simulate waiting and then updating the delay value
        time.sleep(5)
        new_delay_value = 8000
        print(f"Setting new delay value to {new_delay_value}")
        with delay_lock:
            delayValue = new_delay_value

        # Keep the threads running
        triac_thread.join()
        relay_thread.join()
        sensor_thread.join()

    except KeyboardInterrupt:
        print("Program terminated")

    finally:
        cleanup_gpio()
