# Relay Module

Category:
Output / Control

Difficulty:
Intermediate


## What is it?

Relay is an electrically controlled switch.

Arduino can use it to control devices with higher voltage or current.


## Pins


VCC:

Power


GND:

Ground


IN:

Control signal from Arduino



## Example connection


Arduino:


VCC → 5V

GND → GND

IN → D7



## Example projects

- Smart lights
- Automatic fans
- Home automation


## Common mistakes

- Connecting dangerous voltage directly
- Forgetting transistor/driver on some relays
- Using relay without protection


## Safety notes

High-voltage circuits are dangerous.

Only trained users should work with mains electricity.

Pinout Relay Module
| **[Вывод](ca://s?q=Relay_module_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **VCC** | Питание | 5V | 3.3V или 5V (зависит от модуля) |
| **GND** | Земля | GND | GND |
| **IN** | Управляющий сигнал | Digital pin (например D7) | GPIO (например GPIO23) |