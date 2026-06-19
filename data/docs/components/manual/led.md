# LED (Light Emitting Diode)

Category:
Output / Light

Difficulty:
Beginner


## What is it?

LED is a semiconductor component that produces light when electric current passes through it.

It is one of the most common output components in Arduino projects.


## How it works

LED has polarity.

Current should flow in the correct direction.

The longer leg is usually:

Anode (+)

The shorter leg is usually:

Cathode (-)


## Pins


Anode:

Connect to Arduino output pin through a resistor.


Cathode:

Connect to GND.


## Required components

LED

220-330 Ohm resistor


## Example connection


Arduino Uno:

LED long leg → resistor → D13

LED short leg → GND


## Example projects

- Status indicator
- Traffic light
- Smart lamp
- Alarm system


## Programming


LED is usually controlled with:

digitalWrite()


Example:

digitalWrite(LED_PIN, HIGH);

turns LED on.


digitalWrite(LED_PIN, LOW);

turns LED off.



## Common mistakes

- Connecting LED without resistor
- Reversing polarity
- Connecting LED directly between 5V and GND


## Safety notes

A resistor limits current and protects the LED.

📌 Pinout LED
| **[Вывод](ca://s?q=LED_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **Анод (длинная ножка)** | Плюс, вход | Через резистор → цифровой пин (например D13) | Через резистор → GPIO (3.3V логика) |
| **Катод (короткая ножка)** | Минус, земля | GND | GND |

⚙️ Как работает
Ток должен идти от анода к катоду.

При прямом включении LED светится, при обратном — не работает.

На Arduino Uno обычно используют digitalWrite() для включения/выключения.