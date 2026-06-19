"""
Sources: ESP32 official documentation
Saved to: data/docs/esp32/

Primary source: https://docs.espressif.com/projects/arduino-esp32/en/latest/
Raw files:      https://raw.githubusercontent.com/espressif/arduino-esp32/master/docs/en/api/
"""

from . import DocumentSource

_BASE = "https://docs.espressif.com/projects/arduino-esp32/en/latest"
_RAW = "https://raw.githubusercontent.com/espressif/arduino-esp32/master/docs/en/api"
_RAW_DOCS = "https://raw.githubusercontent.com/arduino/docs-content/main"

CATEGORY = "esp32"

def _d(section: str, page_url: str, path: str) -> DocumentSource:
    return DocumentSource(CATEGORY, section, page_url, _RAW, path)

def _dd(section: str, page_url: str,  path: str) -> DocumentSource:
    return DocumentSource(CATEGORY, section, page_url, _RAW_DOCS, path)


SOURCES: list[DocumentSource] = [
    # ------------------------------------------------------------------ #
    # GPIO                                                                 #
    # Отличия от Arduino: INPUT_PULLDOWN, нет ограничения по PWM-пинам,   #
    # GPIO6-11 зарезервированы под flash, GPIO34-39 только вход           #
    # ------------------------------------------------------------------ #
    _d(
        "gpio",
        f"{_BASE}/api/gpio.html",
        "gpio.rst",
    ),

    # ------------------------------------------------------------------ #
    # ADC — аналоговый ввод                                               #
    # Ключевые отличия от Arduino:                                        #
    #   - 12-bit разрешение (0-4095) вместо 10-bit (0-1023)              #
    #   - ADC2 нельзя использовать при активном WiFi                      #
    #   - analogReadResolution() для изменения разрядности                #
    #   - analogSetAttenuation() для диапазона напряжения                 #
    # ------------------------------------------------------------------ #
    _d(
        "adc",
        f"{_BASE}/api/adc.html",
        "adc.rst",
    ),

    # ------------------------------------------------------------------ #
    # PWM / LEDC                                                           #
    # ESP32 не имеет analogWrite() — используется LEDC периферия:         #
    #   - ledcAttach(pin, freq, resolution)                               #
    #   - ledcWrite(pin, dutyCycle)                                       #
    #   - ledcDetach(pin)                                                  #
    #   - до 16 независимых каналов                                       #
    # ------------------------------------------------------------------ #
    _d(
        "pwm",
        f"{_BASE}/api/ledc.html",
        "ledc.rst",
    ),

    # ------------------------------------------------------------------ #
    # DAC — цифро-аналоговый преобразователь                              #
    # Только ESP32 и ESP32-S2, пины GPIO25 и GPIO26                       #
    # dacWrite(pin, value) — 8-bit (0-255)                                #
    # ------------------------------------------------------------------ #
    _d(
        "dac",
        f"{_BASE}/api/dac.html",
        "dac.rst",
    ),

    # ------------------------------------------------------------------ #
    # UART / Serial                                                        #
    # ESP32 имеет 3 аппаратных UART (Serial, Serial1, Serial2)            #
    # Пины можно переназначать через begin(baud, rx, tx)                  #
    # ------------------------------------------------------------------ #
    _dd(
        "uart",
        f"{_BASE}/api/uart.html",
        "content/learn/05.communication/09.uart/uart.md",
    ),

    # ------------------------------------------------------------------ #
    # I2C / Wire                                                           #
    # Дефолтные пины отличаются от Arduino:                               #
    #   SDA = GPIO21, SCL = GPIO22                                        #
    # Поддержка переназначения через Wire.begin(sda, scl)                 #
    # ------------------------------------------------------------------ #
    _d(
        "i2c",
        f"{_BASE}/api/i2c.html",
        "i2c.rst",
    ),

    # ------------------------------------------------------------------ #
    # SPI                                                                  #
    # ESP32: два аппаратных SPI (VSPI и HSPI)                             #
    # Дефолтные пины VSPI: MOSI=23, MISO=19, SCK=18, SS=5                #
    # ------------------------------------------------------------------ #
    _d(
        "spi",
        f"{_BASE}/api/spi.html",
        "spi.rst",
    ),

    # ------------------------------------------------------------------ #
    # WiFi                                                                 #
    # WiFi.begin(), WiFi.connect(), WiFiClient, WiFiServer                #
    # ВАЖНО: при активном WiFi ADC2 недоступен                            #
    # ------------------------------------------------------------------ #
    _d(
        "wifi",
        f"{_BASE}/api/wifi.html",
        "wifi.rst",
    ),

    # ------------------------------------------------------------------ #
    # BLE — Bluetooth Low Energy                                           #
    # Доступен на ESP32, C3, S3                                           #
    # ------------------------------------------------------------------ #
    _d(
        "bluetooth",
        f"{_BASE}/api/ble.html",
        "ble.rst",
    ),

    # ------------------------------------------------------------------ #
    # Preferences — NVS хранилище (замена EEPROM на ESP32)                #
    # Preferences.begin(), putInt(), getInt(), remove()                   #
    # ------------------------------------------------------------------ #
    _d(
        "storage",
        f"{_BASE}/api/preferences.html",
        "preferences.rst",
    ),

    # ------------------------------------------------------------------ #
    # Timer — аппаратные таймеры                                          #
    # timerBegin(), timerAttachInterrupt(), timerAlarm()                  #
    # ------------------------------------------------------------------ #
    _d(
        "timer",
        f"{_BASE}/api/timer.html",
        "timer.rst",
    ),

    # ------------------------------------------------------------------ #
    # Touch — ёмкостные пины (только ESP32 и S2/S3)                      #
    # touchRead(pin) — без внешних компонентов                            #
    # ------------------------------------------------------------------ #
    _d(
        "gpio",
        f"{_BASE}/api/touch.html",
        "touch.rst",
    ),
]