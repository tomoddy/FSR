import math
import serial
import serial.tools.list_ports
import subprocess
import time

THRESHOLD = 5000
DEBOUNCE = 5

PICO_CODE = """
import machine, time
adc = machine.ADC(26)
led = machine.Pin("LED", machine.Pin.OUT)
while True:
    raw = adc.read_u16()
    led.value(raw > %d)
    print(raw)
    time.sleep(0.2)
""" % THRESHOLD


def beep(freq, ms):
    rate = 8000
    samples = bytes(int(128 + 100 * math.sin(2 * math.pi * freq * i / rate)) for i in range(rate * ms // 1000))
    subprocess.run(["paplay", "--raw", "--format=u8", "--rate=" + str(rate), "--channels=1"], input=samples)


PICO_PORTS = [p for p in serial.tools.list_ports.comports() if p.vid == 0x2E8A]
for p in serial.tools.list_ports.comports():
    print(p.device, hex(p.vid) if p.vid else None, p.description)
if not PICO_PORTS:
    raise SystemExit("No Raspberry Pi Pico found")
PORT = PICO_PORTS[0].device
print("Using", PORT)

with serial.Serial(PORT, 115200, timeout=1) as ser:
    ser.write(b"\r\x03\x03\x02")
    time.sleep(0.2)
    ser.write(b"\x05")
    ser.write(PICO_CODE.replace("\n", "\r").encode())
    ser.write(b"\x04")
    print("Running on Pico... Ctrl+C to stop")
    pressed = False
    streak = 0
    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if line:
                print(repr(line))
            if not line.isdigit():
                continue
            raw = int(line)
            high = raw > THRESHOLD
            if high != pressed:
                streak += 1
                if streak >= DEBOUNCE:
                    pressed = high
                    streak = 0
                    print("PRESSED" if pressed else "RELEASED")
                    if not pressed:
                        beep(400, 300)
            else:
                streak = 0
            if pressed:
                beep(1000, 100)
    except KeyboardInterrupt:
        ser.write(b"\x03")
        print("Stopped")