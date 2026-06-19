"""
Sources: Electronic components — datasheets, wiring guides, library READMEs
Saved to: data/docs/components/

Strategy: prefer GitHub raw README/docs over PDF datasheets — they are
text-friendly for RAG and contain code examples alongside specs.

Sections:
  sensors-environmental
  sensors-distance
  sensors-motion
  sensors-light
  sensors-other
  input
  display
  output-motor
  output-led
  output-sound
  storage
  communication
  power
  boards
"""

from . import DocumentSource


CATEGORY = "components"


def _d(section: str, page_url: str, raw_base: str, path: str) -> DocumentSource:
    return DocumentSource(
        CATEGORY,
        section,
        page_url,
        raw_base,
        path
    )


# Raw bases
_ADAFRUIT = "https://raw.githubusercontent.com/adafruit"
_ARDUINO_LIBS = "https://raw.githubusercontent.com/arduino-libraries"
_DFROBOT = "https://raw.githubusercontent.com/DFRobot"
_FASTLED = "https://raw.githubusercontent.com/FastLED/FastLED/master"


SOURCES: list[DocumentSource] = [

# ============================================================
# SENSORS — Environmental
# ============================================================

# DHT11 / DHT22
_d(
    "sensors-environmental",
    "https://github.com/adafruit/DHT-sensor-library",
    _ADAFRUIT,
    "DHT-sensor-library/master/README.md"
),

# BME280
_d(
    "sensors-environmental",
    "https://github.com/adafruit/Adafruit_BME280_Library",
    _ADAFRUIT,
    "Adafruit_BME280_Library/master/README.md"
),

# DS18B20
_d(
    "sensors-environmental",
    "https://github.com/milesburton/Arduino-Temperature-Control-Library",
    "https://raw.githubusercontent.com/milesburton",
    "Arduino-Temperature-Control-Library/master/README.md"
),

# ============================================================
# SENSORS — Distance
# ============================================================

# HC-SR04
_d(
    "sensors-distance",
    "https://github.com/gamegine/HCSR04-ultrasonic-sensor-lib",
    "https://raw.githubusercontent.com/gamegine",
    "HCSR04-ultrasonic-sensor-lib/master/README.md"
),


# VL53L0X
_d(
    "sensors-distance",
    "https://github.com/adafruit/Adafruit_VL53L0X",
    _ADAFRUIT,
    "Adafruit_VL53L0X/master/README.md"
),



# ============================================================
# SENSORS — Motion
# ============================================================

# MPU6050
_d(
    "sensors-motion",
    "https://github.com/ElectronicCats/mpu6050",
    "https://raw.githubusercontent.com/ElectronicCats",
    "mpu6050/master/README.md"
),



# ============================================================
# SENSORS — Light
# ============================================================

# BH1750
_d(
    "sensors-light",
    "https://github.com/claws/BH1750",
    "https://raw.githubusercontent.com/claws",
    "BH1750/master/README.md"
),

# ============================================================
# INPUT
# ============================================================


# Button
_d(
    "input",
    "https://docs.arduino.cc/built-in-examples/digital/Button",
    "https://raw.githubusercontent.com",
    "arduino/docs-content/main/content/built-in-examples/02.digital/Button/Button.md"
),


# Potentiometer
_d(
    "input",
    "https://docs.arduino.cc/tutorials/generic/rotary-potentiometer",
    "https://raw.githubusercontent.com",
    "arduino/docs-content/main/content/learn/04.electronics/08.potentiometer-basics/potentiometer-basics.md"
),



# ============================================================
# DISPLAYS
# ============================================================


# SSD1306 OLED
_d(
    "display",
    "https://github.com/adafruit/Adafruit_SSD1306",
    _ADAFRUIT,
    "Adafruit_SSD1306/master/README.md"
),


# LCD 16x2
_d(
    "display",
    "https://github.com/arduino-libraries/LiquidCrystal",
    _ARDUINO_LIBS,
    "LiquidCrystal/master/README.adoc"
),


# TM1637
_d(
    "display",
    "https://github.com/avishorp/TM1637",
    "https://raw.githubusercontent.com/avishorp",
    "TM1637/master/README.md"
),



# ============================================================
# OUTPUT — Motors
# ============================================================


# Servo
_d(
    "output-motor",
    "https://github.com/arduino-libraries/Servo",
    "https://raw.githubusercontent.com",
    "arduino/docs-content/main/content/learn/04.electronics/05.servo-motors/servo-motors.md"
),

# Stepper
_d(
    "output-motor",
    "https://github.com/arduino-libraries/Stepper",
    _ARDUINO_LIBS,
    "Stepper/master/README.adoc"
),



# ============================================================
# OUTPUT — LED
# ============================================================


# NeoPixel
_d(
    "output-led",
    "https://github.com/adafruit/Adafruit_NeoPixel",
    _ADAFRUIT,
    "Adafruit_NeoPixel/master/README.md"
),


# FastLED
_d(
    "output-led",
    "https://github.com/FastLED/FastLED",
    _FASTLED,
    "README.md"
),



# ============================================================
# OUTPUT — SOUND
# ============================================================


# DFPlayer Mini
_d(
    "output-sound",
    "https://github.com/DFRobot/DFRobotDFPlayerMini",
    _DFROBOT,
    "DFRobotDFPlayerMini/master/README.md"
),



# ============================================================
# STORAGE
# ============================================================


# SD Card
_d(
    "storage",
    "https://github.com/arduino-libraries/SD",
    _ARDUINO_LIBS,
    "SD/master/README.adoc"
),



# ============================================================
# COMMUNICATION
# ============================================================


# nRF24L01
_d(
    "communication",
    "https://github.com/nRF24/RF24",
    "https://raw.githubusercontent.com/nRF24",
    "RF24/master/README.md"
),

# ============================================================
# BOARDS
# ============================================================


# ESP32 Arduino Core
_d(
    "boards",
    "https://github.com/espressif/arduino-esp32",
    "https://raw.githubusercontent.com/espressif",
    "arduino-esp32/master/README.md"
),

]