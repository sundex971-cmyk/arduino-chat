# PIR Motion Sensor

Category:
Sensor / Motion

Difficulty:
Beginner


## What is it?

PIR sensor detects movement using changes in infrared radiation.

It is commonly used in alarm systems and automatic lighting.


## Pins


VCC:

Power.

Usually:
5V


OUT:

Digital signal output.


GND:

Ground.



## Example connection


Arduino Uno:


VCC → 5V

OUT → D2

GND → GND



## How it works

When motion is detected:

OUT becomes HIGH.


When no motion:

OUT becomes LOW.



## Example projects

- Motion alarm
- Automatic light
- Smart security system


## Common mistakes

- Wrong sensitivity adjustment
- Installing near heat sources
- Forgetting warm-up time


## Safety notes

Sensor detects movement, not objects.

Pinout PIR Sensor
| **[Вывод](ca://s?q=PIR_sensor_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **VCC** | Питание | 5V | 3.3V или 5V (зависит от модуля) |
| **OUT** | Цифровой сигнал | Digital pin (например D2) | GPIO (например GPIO4) |
| **GND** | Земля | GND | GND |