"""
Sources: Complete project guides
Saved to: data/docs/projects/

Purpose: give the bot concrete end-to-end examples it can reference when
building the 6-point answer (name / how it works / components / wiring /
alternatives / warnings). Each project should ideally contain:
  - A short description of what the project does
  - A full parts list
  - A wiring / schematic description
  - Working code (or a link to it)
  - Common pitfalls

Sections:
  beginner    — single-concept projects (1 sensor or 1 actuator)
  intermediate — combine 2-3 components, use libraries
  advanced    — networking, data logging, multi-module systems
"""

from . import DocumentSource

CATEGORY = "projects"


def _d(section: str, page_url: str, raw_base: str, path: str) -> DocumentSource:
    return DocumentSource(CATEGORY, section, page_url, raw_base, path)


_ARDUINO_DOCS = "https://raw.githubusercontent.com/arduino/docs-content/main"
_INSTRUCTABLES = "https://www.instructables.com"   # fetch via web_fetch if needed

SOURCES: list[DocumentSource] = [
    # ------------------------------------------------------------------ #
    # BEGINNER                                                             #
    # ------------------------------------------------------------------ #

    # Traffic light (3 LEDs + resistors) — teaches digitalWrite + delay
    # TODO: Arduino project hub or docs-content

    # Temperature monitor (LM35 → Serial) — analogRead + math
    # TODO: docs-content tutorial

    # Distance alarm (HC-SR04 + buzzer) — pulseIn + tone
    # TODO: docs-content tutorial

    # Potentiometer-controlled LED brightness — analogRead + analogWrite
    # Already partially covered by AnalogInOutSerial in arduino.py

    # ------------------------------------------------------------------ #
    # INTERMEDIATE                                                         #
    # ------------------------------------------------------------------ #

    # Smart thermostat (DHT22 + relay + LCD) — sensor + output + display
    # TODO: Arduino project hub

    # Servo sweeper controlled by joystick
    # TODO: docs-content tutorial

    # OLED clock with DS3231 RTC — I2C chaining, time keeping
    # TODO: Arduino project hub

    # Line-following robot (IR sensors + L298N) — digital sensors + motor control
    # TODO: Arduino project hub

    # ------------------------------------------------------------------ #
    # ADVANCED                                                             #
    # ------------------------------------------------------------------ #

    # Data logger (DHT22 + SD card + RTC) — file I/O, timestamps
    # TODO: docs-content or Adafruit learn

    # ESP32 weather station (BME280 + WiFi + ThingSpeak)
    # TODO: Espressif or community tutorial

    # Bluetooth RC car (ESP32 + L298N + mobile app)
    # TODO: community tutorial
]