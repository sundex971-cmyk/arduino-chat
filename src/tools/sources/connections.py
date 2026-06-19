"""
Sources: Wiring/connection diagrams (board + component pairs)
Saved to: data/docs/connections/
 
Purpose: give the bot precise, board-specific pinout examples for the
"C. Схемы подключения" section of answers — e.g. "Arduino Uno + HC-SR04"
vs "ESP32 + HC-SR04" with their different pins and voltage levels.
 
These files are NOT fetched from the web — they are written manually
and placed directly under data/docs/connections/, then picked up by
ingest.py the same way as any other category (via rglob("*.txt")).
 
This module stays empty on purpose so `fetch_docs.py --list` still
shows the "connections" category for consistency, and so a future
web source can be added here without restructuring anything.
 
Naming convention for files in data/docs/connections/:
    <board>_<component>.txt
    e.g. arduino_uno_hc-sr04.txt, esp32_hc-sr04.txt
 
Each file should contain:
    - Board + component name
    - Pin-to-pin wiring list
    - Voltage notes (5V vs 3.3V logic level differences)
    - Any board-specific warnings (e.g. ADC2/WiFi conflict on ESP32)
"""
 
from . import DocumentSource
 
CATEGORY = "connections"
 
SOURCES: list[DocumentSource] = []