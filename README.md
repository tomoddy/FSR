# Bed Occupancy Sensor

ESPHome firmware for a DIY bed occupancy sensor for Home Assistant, built on a Raspberry Pi Pico 2 W with a force-sensitive resistor (FSR) strip.

## Hardware

- Raspberry Pi Pico 2 W
- FSR strip running side to side under the bed at hip height
- 10 kΩ resistor

## Wiring

```
        Raspberry Pi Pico 2 W
       ┌─────────────────────┐
       │                     │
       │  3V3(OUT)  pin 36 ●─┼──────┐
       │                     │      │
       │                     │    ┌─┴─┐
       │                     │    │FSR│  strip under bed
       │                     │    └─┬─┘
       │                     │      │
       │  GP26/ADC0 pin 31 ●─┼──────┤
       │                     │      │
       │                     │    ┌─┴─┐
       │                     │    │10k│  resistor
       │                     │    └─┬─┘
       │                     │      │
       │  GND       pin 38 ●─┼──────┘
       │                     │
       └─────────────────────┘
```

More pressure → lower FSR resistance → higher voltage on GP26 (0–3.3 V).

## How It Works

- The ADC on GP26 is read every 200 ms.
- **Bed Pressure**: voltage averaged over 10 s, reported to Home Assistant.
- **Bed Occupied**: occupancy binary sensor, on above 2.0 V and off below 1.6 V, with a 10 s on-delay and a 5 s off-delay. Mirrored on the onboard LED.

Typical readings: empty ~0 V, items on the bed ~0.9–1.3 V, occupied ~2.5–3.2 V.

## Setup

1. Create `secrets.yaml` (git-ignored):

   ```yaml
   wifi_ssid: ""
   wifi_password: ""
   bed_sensor_api_key: ""      # openssl rand -base64 32
   bed_sensor_ota_password: "" # openssl rand -hex 16
   ```

2. Build:

   ```bash
   esphome compile bed-sensor.yaml
   ```

3. First flash: hold BOOTSEL while plugging in the Pico, then copy the UF2 to the drive:

   ```bash
   cp .esphome/build/bed-sensor/.pioenvs/bed-sensor/firmware.uf2 /media/$USER/RP2350/
   ```

4. Later updates over the air:

   ```bash
   esphome run bed-sensor.yaml --device <pico-ip>
   ```

5. Add to Home Assistant via the ESPHome integration, using the API key.
