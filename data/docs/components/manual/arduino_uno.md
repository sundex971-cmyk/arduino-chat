# Arduino Uno Rev3

Category:
Board / Microcontroller

Difficulty:
Beginner


## What is it?

Arduino Uno Rev3 is a beginner-friendly development board based on the ATmega328P microcontroller.

It allows users to create electronic projects by reading sensors and controlling output devices such as LEDs, motors and displays.


## Main specifications

Microcontroller:
ATmega328P

Operating voltage:
5V

Input voltage:
7-12V recommended

Digital I/O pins:
14

PWM pins:
6

Analog input pins:
6

Flash memory:
32 KB

SRAM:
2 KB


## Pin types


Digital pins:

Used for:
- buttons
- LEDs
- sensors
- communication


PWM pins:

Used for:
- servo motors
- brightness control
- motor speed control


Analog pins:

Used for:
- potentiometers
- analog sensors
- light sensors


## Common connections


LED:

Long leg → resistor → digital pin

Short leg → GND


Button:

One side → 5V

Other side → digital pin

Use pull-down or INPUT_PULLUP


Sensor:

VCC → 5V

GND → GND

Signal → input pin


## Example projects

- Smart lamp
- Temperature monitor
- Parking sensor
- Robot


## Common mistakes

- Connecting 5V directly to GND
- Forgetting GND connection
- Connecting motors directly to GPIO pins


## Safety notes

Arduino pins cannot provide enough current for motors.

Use motor drivers or external power sources.

| **[Пин](ca://s?q=Arduino_Uno_Rev3_digital_pins)** | **Функция** | **Особенности** |
| --- | --- | --- |
| **D0 (RX)** | UART приём | Последовательная связь |
| **D1 (TX)** | UART передача | Последовательная связь |
| **D2** | Digital I/O | Внешнее прерывание INT0 |
| **D3** | Digital I/O | PWM, прерывание INT1 |
| **D4** | Digital I/O | — |
| **D5** | Digital I/O | PWM |
| **D6** | Digital I/O | PWM |
| **D7** | Digital I/O | — |
| **D8** | Digital I/O | — |
| **D9** | Digital I/O | PWM |
| **D10** | Digital I/O | PWM, SPI SS |
| **D11** | Digital I/O | PWM, SPI MOSI |
| **D12** | Digital I/O | SPI MISO |
| **D13** | Digital I/O | SPI SCK, встроенный LED |

| **[Пин](ca://s?q=Arduino_Uno_Rev3_analog_pins)** | **Функция** | **Особенности** |
| --- | --- | --- |
| **A0–A3** | Аналоговые входы | Чтение датчиков |
| **A4** | Аналоговый вход + I²C SDA | Подключение датчиков по I²C |
| **A5** | Аналоговый вход + I²C SCL | Подключение датчиков по I²C |

⚡ Питание и управление
VIN — входное питание (7–12 В).

5V — стабилизированное питание 5 В.

3.3V — питание 3.3 В (ограниченный ток).

GND — земля.

RESET — сброс микроконтроллера.

IOREF — опорное напряжение для логики.

🔗 Интерфейсы
UART: D0 (RX), D1 (TX).

SPI: D10 (SS), D11 (MOSI), D12 (MISO), D13 (SCK).

I²C: A4 (SDA), A5 (SCL).

🛠️ Советы по использованию
PWM-пины (D3, D5, D6, D9, D10, D11) применяются для управления яркостью светодиодов и скоростью моторов.

D13 часто используется для тестов — встроенный LED подключён к этому пину.

A4 и A5 позволяют подключать несколько датчиков через I²C-шину.