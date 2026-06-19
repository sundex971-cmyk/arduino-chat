# HC-SR04 Ultrasonic Distance Sensor

Category:
Sensor / Distance

Difficulty:
Beginner


## What is it?

HC-SR04 is an ultrasonic sensor used to measure distance.

It sends ultrasonic waves and measures the time needed for the echo to return.


## How it works

1. Arduino sends a signal to TRIG.
2. Sensor sends ultrasonic sound.
3. Sound reflects from an object.
4. Sensor receives the echo.
5. Distance is calculated from the travel time.


## Pins


VCC:

Power supply.

Connect:
5V


GND:

Ground.

Connect:
GND


TRIG:

Trigger pin.

Arduino output.

Example:

TRIG → D6


ECHO:

Echo signal.

Arduino input.

Example:

ECHO → D7


## Typical specifications

Voltage:
5V

Measurement range:
approximately 2-400 cm


## Example projects

- Smart parking
- Obstacle detection
- Robot navigation


## Common mistakes

- Forgetting GND
- Wrong TRIG/ECHO direction
- Using without considering voltage differences on ESP32


## ESP32 connection note

HC-SR04 commonly outputs 5V on ECHO.

Use voltage divider before connecting to ESP32 GPIO.

| **[Пин](ca://s?q=HC-SR04_pinout)** | **Назначение** | **Подключение к Arduino** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **VCC** | Питание | 5V | 5V (через VIN или 5V пин) |
| **GND** | Земля | GND | GND |
| **TRIG** | Вход (триггер) | Любой цифровой пин (например D6) | GPIO (3.3V логика) |
| **ECHO** | Выход (сигнал) | Любой цифровой пин (например D7) | GPIO через делитель напряжения (до 3.3V) |

⚙️ Логика работы
На TRIG подаётся импульс 10 мкс.

Датчик излучает ультразвук (40 кГц).

Отражённый сигнал принимается.

На ECHO появляется импульс, длительность которого пропорциональна расстоянию.

Distance = (Time * 343 m/s)/ 2 

🛠️ Советы по подключению
На Arduino Uno можно напрямую подключать TRIG и ECHO.

На ESP32 обязательно использовать резистивный делитель (например, 1 кОм + 2 кОм), чтобы снизить сигнал ECHO до 3.3V.

Всегда проверяйте наличие общей земли (GND) между датчиком и платой.