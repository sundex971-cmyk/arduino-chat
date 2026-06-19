"""
Sources: Rules, best practices, safety guidelines
Saved to: data/docs/rules/

Purpose: ground the bot's "Warnings" and "Alternatives" sections in
documented engineering rules rather than model hallucinations.

These are mostly hand-written Markdown files you create yourself
(stored under data/docs/rules/ directly, not fetched from the web)
plus a few authoritative external references.

Sections:
  electrical-safety   — voltage/current limits, short circuits, ESD
  pin-limits          — max current per pin, 3.3V vs 5V logic levels
  power-supply        — decoupling capacitors, regulator selection
  code-quality        — ISR rules, millis() vs delay(), volatile
  circuit-patterns    — pull-up/pull-down, RC filters, flyback diodes
  common-mistakes     — top beginner errors with explanations
"""

from . import DocumentSource

CATEGORY = "rules"


def _d(section: str, page_url: str, raw_base: str, path: str) -> DocumentSource:
    return DocumentSource(CATEGORY, section, page_url, raw_base, path)


# Rules documents that can be fetched from the web
_ARDUINO_DOCS = "https://raw.githubusercontent.com/arduino/docs-content/main"

SOURCES: list[DocumentSource] = [
    # ------------------------------------------------------------------ #
    # ELECTRICAL SAFETY                                                    #
    # ------------------------------------------------------------------ #
    # TODO: Arduino troubleshooting / protection guide from docs-content

    # ------------------------------------------------------------------ #
    # PIN LIMITS (per official specs)                                      #
    # ------------------------------------------------------------------ #
    # Key facts to encode (as a local hand-written .md if no URL exists): #
    #  - Arduino Uno/Nano pin max current: 40 mA (abs), 20 mA recommended #
    #  - Total I/O current: 200 mA max                                    #
    #  - ESP32 GPIO max: 40 mA per pin, 1200 mA total                    #
    #  - 3.3V GPIO (ESP32, Due, Zero) NOT 5V-tolerant → use level shifter #
    #  - analogWrite (PWM) on Uno: pins 3,5,6,9,10,11 only               #
    # TODO: fetch from hardware datasheets already in arduino.py boards   #

    # ------------------------------------------------------------------ #
    # CODE QUALITY RULES                                                   #
    # ------------------------------------------------------------------ #
    # Key rules to encode:
    #  - Never use delay() when controlling multiple things simultaneously
    #    → use millis() pattern (BlinkWithoutDelay already in arduino.py)
    #  - Variables shared between ISR and main loop MUST be volatile
    #  - ISR must be short — no Serial.print, no delay, no heavy math
    #  - Use unsigned long for millis() timestamps (overflow at 49 days)
    #  - Avoid String class on low-RAM boards (heap fragmentation)
    #  - Always check Serial.available() before Serial.read()
    # TODO: encode as local markdown file

    # ------------------------------------------------------------------ #
    # CIRCUIT PATTERNS                                                     #
    # ------------------------------------------------------------------ #
    # Key patterns to encode:
    #  - Pull-up resistor: button to GND + INPUT_PULLUP (10kΩ internal)
    #  - Pull-down resistor: button to VCC + external 10kΩ to GND
    #  - Current-limiting resistor for LED: R = (Vcc - Vf) / If
    #    (e.g. 5V - 2V) / 0.02A = 150 Ω → use 220 Ω standard
    #  - Flyback diode across motor/relay coil (1N4007, cathode to +)
    #  - Decoupling cap: 100nF ceramic between VCC and GND near IC
    #  - Level shifter for 5V Arduino ↔ 3.3V module (e.g. TXS0108E)
    # TODO: encode as local markdown file

    # ------------------------------------------------------------------ #
    # COMMON BEGINNER MISTAKES                                             #
    # ------------------------------------------------------------------ #
    # Top mistakes to document:
    #  1. Powering servo from Arduino 5V pin → brown-out; use external PSU
    #  2. Connecting LED without resistor → burns LED and/or pin
    #  3. Using delay() in loop → blocks everything, use millis()
    #  4. Reading analogRead() on floating pin → random noise
    #  5. Connecting 5V signal to 3.3V ESP32 GPIO → damages chip
    #  6. Forgetting common GND when using external power supply
    #  7. Using int instead of unsigned long for millis() → overflow bug
    #  8. Not decoupling motor power from logic power → resets
    #  9. Serial.begin() missing → garbage in Serial Monitor
    # 10. Uploading while hardware connected to TX/RX → upload fails
    # TODO: encode as local markdown file
]


# ------------------------------------------------------------------ #
# LOCAL FILES                                                         #
# These are not fetched — create them manually under data/docs/rules/ #
# ------------------------------------------------------------------ #
#
# data/docs/rules/
#   electrical_safety.md      — voltage/current limits, ESD basics
#   pin_limits.md             — per-pin and total current limits by board
#   power_supply.md           — decoupling, regulator tips, separate PSUs
#   code_quality.md           — millis, volatile, ISR rules, String pitfalls
#   circuit_patterns.md       — pull-up/down, LED resistor, flyback, level shift
#   common_mistakes.md        — top-10 beginner errors with fixes
#
# These should be indexed by your RAG pipeline the same way as fetched files.