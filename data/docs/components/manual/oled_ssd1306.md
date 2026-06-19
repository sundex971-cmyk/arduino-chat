# SSD1306 OLED Display

Category:
Display / Output

Difficulty:
Intermediate


## What is it?

SSD1306 OLED is a small display module used to show text, numbers and graphics.

It is commonly connected using I2C.


## Pins


VCC:

Power


GND:

Ground


SCL:

I2C clock


SDA:

I2C data



## Example connection


Arduino Uno:


VCC → 5V

GND → GND

SDA → A4

SCL → A5



## Example projects

- Weather station
- Sensor dashboard
- Smart home display


## Programming


Common libraries:

Adafruit_SSD1306

Adafruit_GFX



## Common mistakes

- Wrong I2C address
- Wrong SDA/SCL pins
- Missing library dependencies


## Safety notes

Check voltage compatibility of the module.

Pinout SSD1306 OLED
| **[Вывод](ca://s?q=SSD1306_OLED_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **VCC** | Питание | 5V | 3.3V или 5V (зависит от модуля) |
| **GND** | Земля | GND | GND |
| **SDA** | I²C данные | A4 | GPIO21 |
| **SCL** | I²C такт | A5 | GPIO22 |