# IR Receiver Module

Category:
Input / Communication

Difficulty:
Beginner


## What is it?

IR receiver allows Arduino to receive commands from infrared remote controls.


## Pins


VCC:

Power


GND:

Ground


Signal:

Digital input



## Example projects

- Remote controlled robot
- Smart lamp
- Media controller


## Programming


Usually uses:

IRremote library



## Common mistakes

- Wrong pin configuration
- Blocking the receiver with objects
- Using unsupported remote protocols

Pinout IR Receiver Module
| **[Вывод](ca://s?q=IR_receiver_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **VCC** | Питание | 5V | 3.3V или 5V (зависит от модуля) |
| **GND** | Земля | GND | GND |
| **Signal** | Цифровой выход | Digital pin (например D11) | GPIO (например GPIO23) |