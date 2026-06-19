# Potentiometer

Category:
Input / Variable Resistor

Difficulty:
Beginner


## What is it?

A potentiometer is a variable resistor.

By turning the knob, the resistance changes.

Arduino can read this change as an analog value.


## Pins


Typical potentiometer has 3 pins.


Left pin:

Connect to:

5V


Right pin:

Connect to:

GND


Middle pin:

Output signal.

Connect to analog input.



## Example connection


Arduino Uno:


Potentiometer left pin → 5V

Potentiometer right pin → GND

Middle pin → A0



## How it works


Arduino analog input reads voltage.

The value is converted into a number.

Arduino Uno:

0-1023 range



## Example projects

- Volume control
- Brightness control
- Robot control
- Menu navigation


## Programming


Usually uses:

analogRead()


Example:

value = analogRead(A0);



## Common mistakes

- Connecting middle pin to power
- Forgetting GND
- Using digital pin instead of analog input


## Safety notes

Potentiometers are usually low-power input devices.

Pinout Potentiometer
| **[Вывод](ca://s?q=Potentiometer_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **Левый** | Питание | 5V | 3.3V |
| **Правый** | Земля | GND | GND |
| **Средний (wiper)** | Сигнал | Analog input (например A0) | GPIO с ADC (например GPIO34) |