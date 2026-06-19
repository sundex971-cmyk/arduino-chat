"""
Sources: Arduino official documentation
Saved to: data/docs/arduino/
"""

from . import DocumentSource

_BASE = "https://docs.arduino.cc"
_DOCS = "https://raw.githubusercontent.com/arduino/docs-content/main"
_REF = "https://raw.githubusercontent.com/arduino/reference-en/master"

CATEGORY = "arduino"


def _d(section: str, page_url: str, raw_base: str, path: str) -> DocumentSource:
    return DocumentSource(CATEGORY, section, page_url, raw_base, path)


SOURCES: list[DocumentSource] = [
    # ------------------------------------------------------------------ #
    # GETTING STARTED                                                      #
    # ------------------------------------------------------------------ #
    _d("getting-started", f"{_BASE}/learn/starting-guide/getting-started-arduino/", _DOCS,
       "content/learn/01.starting-guide/00.getting-started-arduino/getting-started-arduino.md"),
    _d("getting-started", f"{_BASE}/learn/programming/sketches/", _DOCS,
       "content/learn/03.programming/03.sketches/sketches.md"),

    # ------------------------------------------------------------------ #
    # PINS AND I/O                                                         #
    # ------------------------------------------------------------------ #
    _d("pins-and-io", f"{_BASE}/learn/microcontrollers/digital-pins/", _DOCS,
       "content/learn/02.microcontrollers/01.digital-pins/digital-pins.md"),
    _d("pins-and-io", f"{_BASE}/learn/microcontrollers/analog-input/", _DOCS,
       "content/learn/02.microcontrollers/02.analog-input/analog-input.md"),
    _d("pins-and-io", f"{_BASE}/learn/microcontrollers/analog-output/", _DOCS,
       "content/learn/02.microcontrollers/03.analog-output/analog-output.md"),

    # ------------------------------------------------------------------ #
    # PROGRAMMING BASICS                                                   #
    # ------------------------------------------------------------------ #
    _d("programming-basics", f"{_BASE}/learn/programming/reference/", _DOCS,
       "content/learn/03.programming/00.reference/reference.md"),
    _d("programming-basics", f"{_BASE}/learn/programming/variables/", _DOCS,
       "content/learn/03.programming/01.variables/variables.md"),
    _d("programming-basics", f"{_BASE}/learn/programming/functions/", _DOCS,
       "content/learn/03.programming/02.functions/functions.md"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — overview                                        #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/", _DOCS,
       "content/programming/01.language-reference/language-reference.md"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Sketch structure                                #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/structure/sketch/setup/", _REF,
       "Language/Structure/Sketch/setup.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/sketch/loop/", _REF,
       "Language/Structure/Sketch/loop.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Control structures                              #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/structure/control-structure/if/", _REF,
       "Language/Structure/Control Structure/if.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/control-structure/for/", _REF,
       "Language/Structure/Control Structure/for.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/control-structure/while/", _REF,
       "Language/Structure/Control Structure/while.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/control-structure/dowhile/", _REF,
       "Language/Structure/Control Structure/doWhile.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/control-structure/switch/", _REF,
       "Language/Structure/Control Structure/switchCase.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/control-structure/break/", _REF,
       "Language/Structure/Control Structure/break.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/control-structure/return/", _REF,
       "Language/Structure/Control Structure/return.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Arithmetic & Boolean operators                  #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/structure/arithmetic-operators/addition/", _REF,
       "Language/Structure/Arithmetic Operators/addition.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/arithmetic-operators/subtraction/", _REF,
       "Language/Structure/Arithmetic Operators/subtraction.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/arithmetic-operators/multiplication/", _REF,
       "Language/Structure/Arithmetic Operators/multiplication.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/arithmetic-operators/division/", _REF,
       "Language/Structure/Arithmetic Operators/division.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/boolean-operators/logicaland/", _REF,
       "Language/Structure/Boolean Operators/logicalAnd.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/boolean-operators/logicalor/", _REF,
       "Language/Structure/Boolean Operators/logicalOr.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/structure/boolean-operators/logicalnot/", _REF,
       "Language/Structure/Boolean Operators/logicalNot.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Data types                                      #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/int/", _REF,
       "Language/Variables/Data Types/int.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/long/", _REF,
       "Language/Variables/Data Types/long.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/float/", _REF,
       "Language/Variables/Data Types/float.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/bool/", _REF,
       "Language/Variables/Data Types/bool.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/byte/", _REF,
       "Language/Variables/Data Types/byte.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/char/", _REF,
       "Language/Variables/Data Types/char.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/string/", _REF,
       "Language/Variables/Data Types/string.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/stringobject/", _REF,
       "Language/Variables/Data Types/stringObject.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/array/", _REF,
       "Language/Variables/Data Types/array.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/unsigned-int/", _REF,
       "Language/Variables/Data Types/unsignedInt.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/data-types/unsigned-long/", _REF,
       "Language/Variables/Data Types/unsignedLong.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Constants                                       #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/variables/constants/highlow/", _REF,
       "Language/Variables/Constants/highLow.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/constants/inputoutput/", _REF,
       "Language/Variables/Constants/inputOutputPullup.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/constants/integerconstants/", _REF,
       "Language/Variables/Constants/integerConstants.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/constants/floatingpointconstants/", _REF,
       "Language/Variables/Constants/floatingPointConstants.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Variable scope & qualifiers                     #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/variables/variable-scope-qualifiers/scope/", _REF,
       "Language/Variables/Variable Scope & Qualifiers/scope.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/variable-scope-qualifiers/volatile/", _REF,
       "Language/Variables/Variable Scope & Qualifiers/volatile.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/variable-scope-qualifiers/const/", _REF,
       "Language/Variables/Variable Scope & Qualifiers/const.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/variables/variable-scope-qualifiers/static/", _REF,
       "Language/Variables/Variable Scope & Qualifiers/static.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Digital I/O                                     #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/digital-io/pinMode/", _REF,
       "Language/Functions/Digital IO/pinMode.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/digital-io/digitalread/", _REF,
       "Language/Functions/Digital IO/digitalRead.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/digital-io/digitalwrite/", _REF,
       "Language/Functions/Digital IO/digitalWrite.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Analog I/O                                      #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/analog-io/analogRead/", _REF,
       "Language/Functions/Analog IO/analogRead.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/analog-io/analogWrite/", _REF,
       "Language/Functions/Analog IO/analogWrite.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/analog-io/analogReference/", _REF,
       "Language/Functions/Analog IO/analogReference.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Advanced I/O                                    #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/advanced-io/tone/", _REF,
       "Language/Functions/Advanced IO/tone.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/advanced-io/noTone/", _REF,
       "Language/Functions/Advanced IO/noTone.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/advanced-io/pulseIn/", _REF,
       "Language/Functions/Advanced IO/pulseIn.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/advanced-io/shiftOut/", _REF,
       "Language/Functions/Advanced IO/shiftOut.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/advanced-io/shiftIn/", _REF,
       "Language/Functions/Advanced IO/shiftIn.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Time                                            #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/time/delay/", _REF,
       "Language/Functions/Time/delay.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/time/millis/", _REF,
       "Language/Functions/Time/millis.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/time/micros/", _REF,
       "Language/Functions/Time/micros.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/time/delayMicroseconds/", _REF,
       "Language/Functions/Time/delayMicroseconds.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Interrupts                                      #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/external-interrupts/attachInterrupt/", _REF,
       "Language/Functions/External Interrupts/attachInterrupt.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/external-interrupts/detachInterrupt/", _REF,
       "Language/Functions/External Interrupts/detachInterrupt.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/interrupts/interrupts/", _REF,
       "Language/Functions/Interrupts/interrupts.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/interrupts/noInterrupts/", _REF,
       "Language/Functions/Interrupts/noInterrupts.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Math                                            #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/math/map/", _REF,
       "Language/Functions/Math/map.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/math/constrain/", _REF,
       "Language/Functions/Math/constrain.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/math/abs/", _REF,
       "Language/Functions/Math/abs.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/math/min/", _REF,
       "Language/Functions/Math/min.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/math/max/", _REF,
       "Language/Functions/Math/max.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/math/pow/", _REF,
       "Language/Functions/Math/pow.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/math/sqrt/", _REF,
       "Language/Functions/Math/sqrt.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/random-numbers/random/", _REF,
       "Language/Functions/Random Numbers/random.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/random-numbers/randomSeed/", _REF,
       "Language/Functions/Random Numbers/randomSeed.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Bits & Bytes                                    #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/bits-and-bytes/bitRead/", _REF,
       "Language/Functions/Bits and Bytes/bitRead.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/bits-and-bytes/bitWrite/", _REF,
       "Language/Functions/Bits and Bytes/bitWrite.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/bits-and-bytes/bitSet/", _REF,
       "Language/Functions/Bits and Bytes/bitSet.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/bits-and-bytes/bitClear/", _REF,
       "Language/Functions/Bits and Bytes/bitClear.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/bits-and-bytes/highByte/", _REF,
       "Language/Functions/Bits and Bytes/highByte.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/bits-and-bytes/lowByte/", _REF,
       "Language/Functions/Bits and Bytes/lowByte.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Serial                                          #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/", _REF,
       "Language/Functions/Communication/Serial.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/begin/", _REF,
       "Language/Functions/Communication/Serial/begin.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/available/", _REF,
       "Language/Functions/Communication/Serial/available.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/read/", _REF,
       "Language/Functions/Communication/Serial/read.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/print/", _REF,
       "Language/Functions/Communication/Serial/print.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/println/", _REF,
       "Language/Functions/Communication/Serial/println.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/write/", _REF,
       "Language/Functions/Communication/Serial/write.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/parseInt/", _REF,
       "Language/Functions/Communication/Serial/parseInt.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/parseFloat/", _REF,
       "Language/Functions/Communication/Serial/parseFloat.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/readString/", _REF,
       "Language/Functions/Communication/Serial/readString.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/end/", _REF,
       "Language/Functions/Communication/Serial/end.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/serial/flush/", _REF,
       "Language/Functions/Communication/Serial/flush.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — Wire / I2C                                      #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/wire/", _REF,
       "Language/Functions/Communication/Wire.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/wire/begin/", _REF,
       "Language/Functions/Communication/Wire/begin.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/wire/requestFrom/", _REF,
       "Language/Functions/Communication/Wire/requestFrom.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/wire/beginTransmission/", _REF,
       "Language/Functions/Communication/Wire/beginTransmission.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/wire/endTransmission/", _REF,
       "Language/Functions/Communication/Wire/endTransmission.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/wire/write/", _REF,
       "Language/Functions/Communication/Wire/write.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/wire/available/", _REF,
       "Language/Functions/Communication/Wire/available.adoc"),
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/wire/read/", _REF,
       "Language/Functions/Communication/Wire/read.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — SPI                                             #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/communication/SPI/", _REF,
       "Language/Functions/Communication/SPI.adoc"),

    # ------------------------------------------------------------------ #
    # LANGUAGE REFERENCE — EEPROM                                          #
    # ------------------------------------------------------------------ #
    _d("language-reference", f"{_BASE}/language-reference/en/functions/eeprom/", _DOCS,
       "content/learn/07.built-in-libraries/03.eeprom/eeprom.md"),

    # ------------------------------------------------------------------ #
    # BOARDS                                                               #
    # ------------------------------------------------------------------ #
    _d("boards", f"{_BASE}/hardware/uno-rev3/", _DOCS,
       "content/hardware/02.uno/boards/uno-rev3/tutorials/board-anatomy/content.md"),
    _d("boards", f"{_BASE}/hardware/nano/", _DOCS,
       "content/hardware/03.nano/boards/nano/datasheet/datasheet.md"),
    _d("boards", f"{_BASE}/hardware/mega2560/", _DOCS,
       "content/hardware/10.mega/boards/mega-2560/tutorials/getting-started/getting-started.md"),

    # ------------------------------------------------------------------ #
    # TUTORIALS                                                            #
    # ------------------------------------------------------------------ #
    _d("tutorials", f"{_BASE}/built-in-examples/basics/Blink/", _DOCS,
       "content/built-in-examples/01.basics/Blink/Blink.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/basics/Fade/", _DOCS,
       "content/built-in-examples/01.basics/Fade/Fade.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/digital/Button/", _DOCS,
       "content/built-in-examples/02.digital/Button/Button.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/digital/Debounce/", _DOCS,
       "content/built-in-examples/02.digital/Debounce/Debounce.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/digital/InputPullupSerial/", _DOCS,
       "content/built-in-examples/02.digital/InputPullupSerial/InputPullupSerial.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/digital/BlinkWithoutDelay/", _DOCS,
       "content/built-in-examples/02.digital/BlinkWithoutDelay/BlinkWithoutDelay.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/digital/toneKeyboard/", _DOCS,
       "content/built-in-examples/02.digital/toneKeyboard/toneKeyboard.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/analog/AnalogReadSerial/", _DOCS,
       "content/built-in-examples/01.basics/AnalogReadSerial/AnalogReadSerial.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/analog/AnalogInOutSerial/", _DOCS,
       "content/built-in-examples/03.analog/AnalogInOutSerial/AnalogInOutSerial.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/analog/Smoothing/", _DOCS,
       "content/built-in-examples/03.analog/Smoothing/Smoothing.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/communication/ASCIITable/", _DOCS,
       "content/built-in-examples/04.communication/ASCIITable/ASCIITable.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/communication/SerialEvent/", _DOCS,
       "content/built-in-examples/04.communication/SerialEvent/SerialEvent.md"),
    _d("tutorials", f"{_BASE}/built-in-examples/servo/Knob/", _DOCS,
       "content/hardware/11.modulino/modulino-nodes/modulino-knob/tutorials/how-knob/content.md"),
]
