# DS3231 Real Time Clock Module

Category:
Module / Time

Difficulty:
Intermediate


## What is it?

DS3231 is a real-time clock module.

It keeps accurate time even when Arduino is powered off.


## Communication

Uses:

I2C



## Pins


VCC:

Power


GND:

Ground


SDA:

I2C data


SCL:

I2C clock



## Example projects

- Digital clock
- Data logger
- Scheduled automation


## Programming


Common libraries:

RTClib



## Common mistakes

- Wrong I2C pins
- Missing battery
- Incorrect time setup

Pinout DS3231 RTC Module
| **[Вывод](ca://s?q=DS3231_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **VCC** | Питание | 5V | 3.3V или 5V (зависит от модуля) |
| **GND** | Земля | GND | GND |
| **SDA** | I²C данные | A4 | GPIO21 |
| **SCL** | I²C такт | A5 | GPIO22 |