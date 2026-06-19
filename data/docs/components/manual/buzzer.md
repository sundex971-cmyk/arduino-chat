# Buzzer / Piezo Buzzer

Category:
Output / Sound

Difficulty:
Beginner


## What is it?

A buzzer is an electronic component that produces sound.

It can be used for alarms, notifications and simple melodies.


## Types


Active buzzer:

Produces sound when voltage is applied.


Passive buzzer:

Needs a frequency signal.

Can play different tones.


## Pins


Positive (+):

Connect to Arduino output pin.


Negative (-):

Connect to GND.


## Example connection


Arduino Uno:


Buzzer + → D8

Buzzer - → GND



## Programming


Passive buzzer can use:

tone()


Example:

tone(8, 1000);


Creates a sound with frequency 1000 Hz.



## Example projects

- Alarm system
- Door sensor
- Timer
- Musical projects


## Common mistakes

- Connecting polarity incorrectly
- Using wrong buzzer type
- Expecting passive buzzer to work without tone()


## Safety notes

Small buzzers can be powered from Arduino pins.

Large speakers require additional hardware.

Pinout Buzzer
| **[Вывод](ca://s?q=Buzzer_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **Плюс (+)** | Вход питания/сигнал | Digital pin (например D8) | GPIO (PWM) |
| **Минус (–)** | Земля | GND | GND |