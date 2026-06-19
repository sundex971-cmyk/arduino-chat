# Push Button

Category:
Input / Control

Difficulty:
Beginner


## What is it?

A push button is a simple input component.

It connects two electrical points when pressed.

Arduino can detect the press and perform an action.


## How it works

When the button is pressed:

Circuit is closed.

Arduino receives a HIGH or LOW signal depending on the wiring.


## Pins

Most simple buttons have 4 legs.

Two opposite sides are internally connected.


## Example connection


Using pull-down resistor:


Button side 1:

→ 5V


Button side 2:

→ Digital pin (example D2)

and

→ 10K resistor → GND



## Arduino alternative

Internal pull-up resistor can be used:

pinMode(buttonPin, INPUT_PULLUP);


In this mode:

Pressed:
LOW

Released:
HIGH


## Example projects

- Start button
- Light switch
- Game controller
- Alarm activation


## Common mistakes

- Connecting wrong button legs
- Forgetting pull-up/pull-down resistor
- Reading unstable signals


## Extra note

Mechanical buttons can create multiple signals when pressed.

This effect is called bouncing.

For accurate projects use debounce techniques.

Pinout Push Button
| **[Вывод](ca://s?q=Push_Button_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **Ножка 1** | Вход питания | 5V | 3.3V или 5V (через VIN) |
| **Ножка 2** | Сигнал | Digital pin (например D2) | GPIO |
| **Ножка 3** | Соединена с ножкой 1 | — | — |
| **Ножка 4** | Соединена с ножкой 2 | — | — |