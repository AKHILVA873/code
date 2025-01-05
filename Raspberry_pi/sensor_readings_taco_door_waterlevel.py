import RPi.GPIO as GPIO
import spidev
import time
from hx711 import HX711

# Pin definitions
DOUT_PIN = 21  # GPIO 21
PD_SCK_PIN = 20  # GPIO 20
DIGITAL_PIN = 4  # GPIO 4 (changed from reserved pin)
ANALOG_CHANNEL = 0  # MCP3008 channel 0

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
GPIO.setup(DIGITAL_PIN, GPIO.IN)

def read_adc(channel):
    if channel < 0 or channel > 7:
        raise ValueError('Channel must be between 0 and 7')
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

def read_hx711():
    return hx.get_weight(5)  # Get the average of 5 readings

def main():
    try:
        while True:
            # Read from HX711
            count = read_hx711()
            voltage = (count / 16777216.0) * 5.0  # Convert count to voltage

            # Assuming the pressure sensor's voltage output is proportional to water depth
            water_level = voltage * 10.0  # Example conversion factor, adjust as needed
            
            print(f"watersensor: {voltage:.3f}")

            # Read analog value from MCP3008
            analog_value = read_adc(ANALOG_CHANNEL)
            print(f"taccosensor: {analog_value}")

            # Read digital pin value
            digital_value = GPIO.input(DIGITAL_PIN)
            print(f"doorssensor: {digital_value}")

            time.sleep(0.5)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
