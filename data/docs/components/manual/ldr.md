# LDR / Photoresistor

Category:
Sensor / Light

Difficulty:
Beginner


## What is it?

LDR is a light-dependent resistor.

Its resistance changes depending on the amount of light.


## How it works

More light:

Lower resistance


Less light:

Higher resistance


Arduino reads the voltage change using analog input.


## Connection


Requires voltage divider.


Example:


5V

|

LDR

|

Analog pin A0

|

Resistor

|

GND



## Example projects

- Automatic lamp
- Light meter
- Smart curtains


## Programming


Uses:

analogRead()



Arduino Uno:

0-1023 values



## Common mistakes

- Connecting directly without resistor
- Using digital pin instead of analog

Pinout LDR
| **[Вывод](ca://s?q=LDR_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **Вывод 1** | Один конец резистора | 5V | 3.3V |
| **Вывод 2** | Второй конец резистора | Аналоговый вход (например A0) через делитель | GPIO с ADC (например GPIO34) |