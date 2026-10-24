import machine
import time

# Initialize ADC on GPIO 26 (ADC0 / Pin 31)
adc = machine.ADC(26)

# The Pico 2 W uses a 16-bit ADC (values from 0 to 65535)
# This converts the raw reading into an easy-to-read voltage (0V to 3.3V)
CONVERSION_FACTOR = 3.3 / 65535

print("FSR Pressure Monitor Started. Press the sensor!")

while True:
    raw_value = adc.read_u16()
    voltage = raw_value * CONVERSION_FACTOR
    
    # Print both the raw digital value and the corresponding voltage
    print(f"Raw Reading: {raw_value:5d} | Voltage: {voltage:.2f}V")
    
    # Pause for 0.2 seconds between readings so the shell isn't flooded
    time.sleep(0.2)