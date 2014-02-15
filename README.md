# Arduino-Lufa
=========================

LUFA (Lightweight USB For AVRs) on the Arduino!

## Description

Modern Arduinos ([Arduino Leonardo], [Arduino Micro], [Arduino Esplora], [Arduino Lilypad USB], and the Upcoming [Arduino Tre]) came with a ATmega32u4 which have a native USB interface on the MCU. The Arduino IDE also came with a tiny USB stack that has a USB CDC Serial, a Keyboard, and a Mouse. It might be enough if you're migrating old projects (form ATmega168/328's) to the new hardware, but when you want to unleash the full power of it, you'd find that the current implementations lasks extensibility (BADLY!).

Thus, I managed to bring the powerful [LUFA] to Arduino!

[Arduino Leonardo]:http://arduino.cc/en/Main/ArduinoBoardLeonardo
[Arduino Micro]:http://arduino.cc/en/Main/ArduinoBoardMicro
[Arduino Esplora]:http://arduino.cc/en/Main/ArduinoBoardEsplora#.Uv9QRNySzkI
[Arduino Lilypad USB]:http://arduino.cc/en/Main/ArduinoBoardLilyPadUSB
[Arduino Tre]:http://arduino.cc/en/Main/ArduinoBoardTre

[LUFA]:http://www.fourwalledcubicle.com/LUFA.php

## Installation
The installation is quiet tricky, because the stock USB stack is in the arduino core directory instead of a seperated library directory, so you cannot simply drop [Arduino-Lufa] to the library folder under your Sketchbook directory.

There are some more setups besides that...

1. clone the repository, drop in your `<Sketchbook>/libraries` (for instance, you should have `Sketchbook/libraries/LUFA/LUFA.h` after this step.
2. download [LUFA], put everything under `LUFA/` to `<Sketchbook>/libraries/LUFA/LUFA` (for instance, you should have `<Sketchbook>/libraries/LUFA/LUFA/Drivers/USB/USB.h` after this step)
3. delete the stock USB stack from Arduino environment, there are 6 files to be deleted:
  1. `Arduino/hardware/arduino/avr/cores/arduino/CDC.cpp`
  2. `Arduino/hardware/arduino/avr/cores/arduino/HID.cpp`
  3. `Arduino/hardware/arduino/avr/cores/arduino/USBApi.h`
  4. `Arduino/hardware/arduino/avr/cores/arduino/USBCore.cpp`
  5. `Arduino/hardware/arduino/avr/cores/arduino/USBCore.h`
  6. `Arduino/hardware/arduino/avr/cores/arduino/USBDesc.h`
4. edit these 3 files to remove all USB related stuff (if you just dunno how, replace them with the files from `ArduinoHardwareAVR` folder):
  1. `Arduino/hardware/arduino/avr/cores/arduino/Arduino.h`
    * 222: `#include "USBAPI.h"`
    * 223: `#if defined(HAVE_HWSERIAL0) && defined(HAVE_CDCSERIAL)`
    * 224: `#error "Targets with both UART0 and CDC serial not supported"`
    * 225: `#endif`
  2. `Arduino/hardware/arduino/avr/cores/arduino/main.cpp`
    * 26: `#if defined(USBCON)`
    * 27: `USBDevice.attach();`
    * 28: `#endif`
  3. `Arduino/hardware/arduino/avr/cores/arduino/Platform.h`
    * 17: `#if defined(USBCON)`
    * 18: `#include "USBDesc.h"`
	* 19: `#include "USBCore.h"`
	* 20: `#include "USBAPI.h"`
    * 21: `#endif /* if defined(USBCON) */`

That's it! You can now try start the Arduino IDE and compile the examples! :-)

[Arduino-Lufa]:https://github.com/Palatis/Arduino-Lufa

## Credits
* Victor Tseng: palatis _AT_ gmail _DOT_ com
* Arduino: http://arduino.cc
* LUFA: http://www.fourwalledcubicle.com/LUFA.php

## Copying
    The MIT License (MIT)

    Copyright (c) 2014, Victor Tseng

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
