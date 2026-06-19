# ESP32 Development Board

Category:
Board / Microcontroller

Difficulty:
Intermediate


## What is it?

ESP32 is a powerful microcontroller platform with built-in WiFi and Bluetooth.

It is commonly used for IoT, smart home and wireless projects.


## Main specifications

Processor:
32-bit Xtensa LX6

Operating voltage:
3.3V logic

GPIO:
Up to 34 programmable GPIO pins

Wireless:

WiFi:
2.4 GHz

Bluetooth:
Classic Bluetooth + BLE


## Important difference from Arduino Uno

Arduino Uno uses 5V logic.

ESP32 uses 3.3V logic.

Do not connect 5V signals directly to ESP32 GPIO pins.


## Pins


GPIO:

Used for:
- sensors
- LEDs
- buttons


ADC:

Used for reading analog sensors.


PWM:

Used for:
- LEDs
- motors
- servos


I2C:

Used for:
- OLED displays
- sensors


SPI:

Used for:
- displays
- SD cards


## Example projects

- Smart home
- Weather station
- WiFi sensor
- Remote controller


## Common mistakes

- Connecting 5V output to GPIO
- Using unavailable boot pins
- Forgetting common GND


## Safety notes

Always check voltage compatibility before connecting modules.

📌 Основные выводы питания и управления
VIN — входное питание 5–10V (обычно от USB или внешнего источника).

3V3 — стабилизированное питание 3.3V для периферии.

GND — земля.

EN (Enable) — сброс/включение микроконтроллера.

BOOT (GPIO0) — используется для входа в режим прошивки

| **[Интерфейс](ca://s?q=ESP32_Devkit_V1_interfaces)** | **Пины** | **Назначение** |
| --- | --- | --- |
| **UART0** | GPIO1 (TX), GPIO3 (RX) | Основной порт для прошивки и связи |
| **SPI** | GPIO18 (SCK), GPIO19 (MISO), GPIO23 (MOSI), GPIO5 (SS) | Работа с дисплеями, SD‑картами |
| **I²C** | GPIO21 (SDA), GPIO22 (SCL) | Подключение датчиков, OLED |
| **PWM** | Почти любой GPIO (до 16 каналов) | Управление яркостью, моторами |
| **ADC** | GPIO32–39 | Аналоговые входы (12‑бит) |
| **DAC** | GPIO25, GPIO26 | ЦАП‑выходы (аналоговый сигнал) |
| **Touch** | GPIO0, 2, 4, 12–15, 27, 32, 33 | Сенсорные входы |

⚠️ Особые пины (Boot/Flash)
Некоторые GPIO влияют на загрузку:

GPIO0 — режим прошивки.

GPIO2 — встроенный LED, должен быть LOW при старте.

GPIO12 — если HIGH при старте → сбой загрузки.

GPIO15 — должен быть HIGH при старте.

GPIO34–39 — только входы (без выхода).

| **[GPIO](ca://s?q=ESP32_Devkit_V1_GPIO_reference)** | **Функция** |
| --- | --- |
| GPIO0 | Boot, Touch |
| GPIO1 | UART TX |
| GPIO2 | LED, Touch |
| GPIO3 | UART RX |
| GPIO4 | I/O, Touch |
| GPIO5 | SPI SS |
| GPIO12–15 | ADC, Touch, Boot‑чувствительные |
| GPIO16–17 | General I/O |
| GPIO18 | SPI SCK |
| GPIO19 | SPI MISO |
| GPIO21 | I²C SDA |
| GPIO22 | I²C SCL |
| GPIO23 | SPI MOSI |
| GPIO25–27 | ADC/DAC/Touch |
| GPIO32–33 | ADC/Touch |
| GPIO34–39 | ADC (только вход) |

🛠️ Советы по использованию
Всегда проверяйте уровень напряжения: GPIO работают только с 3.3V.

Для подключения датчиков на 5V используйте логические преобразователи.

Не используйте GPIO6–11 — они заняты встроенной SPI‑флеш памятью.

Для простых проектов удобно начинать с GPIO21/22 (I²C) и GPIO18/19/23 (SPI).