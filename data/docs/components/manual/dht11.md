# DHT11 Temperature and Humidity Sensor

Category:
Sensor / Environmental

Difficulty:
Beginner


## What is it?

DHT11 is a digital sensor used to measure temperature and humidity.

It is commonly used in weather stations and smart home projects.


## What it measures

Temperature

Humidity


## Pins


VCC:

Power.

Connect:
5V


DATA:

Digital communication pin.

Connect:
Arduino digital pin


GND:

Ground.

Connect:
GND



## Example connection


Arduino Uno:


VCC → 5V

DATA → D2

GND → GND



## Example projects

- Weather station
- Smart greenhouse
- Room monitor


## Programming


Usually uses:

DHT library


Functions:

readTemperature()

readHumidity()



## Common mistakes

- Reading sensor too frequently
- Wrong sensor type selected
- Missing power connection


## Safety notes

DHT11 is a low-power sensor.

It should not be connected directly to high voltage.

📌 Pinout DHT11
| **[Вывод](ca://s?q=DHT11_pinout)** | **Назначение** | **Подключение к Arduino Uno** | **Подключение к ESP32** |
| --- | --- | --- | --- |
| **VCC** | Питание | 5V | 3.3V или 5V (зависит от модуля) |
| **DATA** | Цифровой сигнал | Digital pin (например D2) | GPIO (например GPIO4) |
| **GND** | Земля | GND | GND |