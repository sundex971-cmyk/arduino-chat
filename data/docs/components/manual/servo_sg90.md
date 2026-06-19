# SG90 Micro Servo Motor

Category:
Output / Motor

Difficulty:
Beginner


## What is it?

SG90 is a small servo motor used to control position.

Unlike DC motors, a servo can move to a specific angle.


## Pins


Wire colors may vary.

Typical:

Brown/Black:

GND


Red:

Power

Usually:
5V


Orange/Yellow:

Signal

Connect to PWM pin


## How it works

The controller sends PWM signals.

The servo changes its position according to the signal.


## Example connection

Arduino Uno:

Servo VCC → 5V

Servo GND → GND

Signal → D9


## Example projects

- Automatic door
- Parking barrier
- Robot arm
- Camera mount


## Common mistakes

- Powering multiple servos from Arduino 5V
- Forgetting GND
- Connecting signal to wrong pin


## Safety notes

Servos can consume significant current.

For multiple servos use external power supply.

📌 Pinout SG90
| **[Провод](ca://s?q=SG90_servo_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **Коричневый/Чёрный** | GND | GND | GND |
| **Красный** | VCC (питание) | 5V | 5V (через VIN или внешний источник) |
| **Оранжевый/Жёлтый** | Signal (PWM) | Любой PWM‑пин (например D9) | GPIO с поддержкой PWM (например GPIO18) |

⚙️ Как работает
Контроллер посылает PWM‑сигнал с периодом ~20 мс.

Длительность импульса (обычно 1–2 мс) задаёт угол поворота:

~1 мс → 0°

~1.5 мс → 90°

~2 мс → 180°

🛠️ Советы по подключению
Один SG90 можно питать от Arduino Uno напрямую.

Несколько сервоприводов требуют внешнего источника питания (например, отдельный 5V блок питания).

Всегда соединяйте общую землю (GND) между Arduino/ESP32 и внешним источником.

На ESP32 используйте GPIO с поддержкой PWM (ESP32 позволяет назначать PWM почти на любой вывод).

⚠️ Частые ошибки
Подключение нескольких SG90 к 5V Arduino без внешнего питания → перегрузка.

Забытый GND → сигнал не будет работать.

Подключение сигнала к не‑PWM пину на Arduino Uno → мотор не реагирует.