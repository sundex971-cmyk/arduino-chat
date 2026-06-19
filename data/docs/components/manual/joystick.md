# Joystick Module

Category:
Input / Control

Difficulty:
Beginner


## What is it?

Joystick module contains two potentiometers and a button.

It provides X and Y position values.


## Pins


VRx:

X axis analog output


VRy:

Y axis analog output


SW:

Button output


VCC:

Power


GND:

Ground



## Example connection


VRx → A0

VRy → A1

SW → D2



## Example projects

- Robot controller
- Game controller
- Camera control


## Programming


Uses:

analogRead()



## Common mistakes

- Wrong calibration
- Using digitalRead for analog axes

Pinout Joystick Module
| **[Вывод](ca://s?q=Joystick_module_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **VRx** | Аналоговый выход X‑оси | A0 | GPIO34 (ADC) |
| **VRy** | Аналоговый выход Y‑оси | A1 | GPIO35 (ADC) |
| **SW** | Кнопка (цифровой выход) | D2 | GPIO23 |
| **VCC** | Питание | 5V | 3.3V или 5V (зависит от модуля) |
| **GND** | Земля | GND | GND |