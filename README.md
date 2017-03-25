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

    The following setup was last tested with arduino-1.8.2 and LUFA 151115 
    (but it should work with future versions, if there were no major changes)

You will neded to modify your arduino installation, so I recommend to create a backup, naming it "arduino-x.x.x_LUFA". (x.x.x. beeing your version number, e.G. 1.8.2)

    You should not use the modified arduino version for non LUFA projects.


1. clone the repository, drop it in your `arduino-x.x.x_LUFA/libraries` (for instance, you should have `arduino-x.x.x_LUFA/libraries/LUFA/LUFA.h` after this step.
2. download [LUFA], put everything under `LUFA/` to `arduino-x.x.x_LUFA/libraries/LUFA/LUFA` (for instance, you should have `arduino-x.x.x_LUFA/libraries/LUFA/LUFA/Drivers/USB/USB.h` after this step)
3. delete the stock USB stack from Arduino environment, there are 7 files to be deleted:
    1. `arduino-x.x.x_LUFA/hardware/arduino/avr/cores/arduino/CDC.cpp`
    2. `arduino-x.x.x_LUFA/hardware/arduino/avr/cores/arduino/PluggableUSB.cpp`
    3. `arduino-x.x.x_LUFA/hardware/arduino/avr/cores/arduino/PluggableUSB.h`
    4. `arduino-x.x.x_LUFA/hardware/arduino/avr/cores/arduino/USBApi.h`
    5. `arduino-x.x.x_LUFA/hardware/arduino/avr/cores/arduino/USBCore.cpp`
    6. `arduino-x.x.x_LUFA/hardware/arduino/avr/cores/arduino/USBCore.h`
    7. `arduino-x.x.x_LUFA/hardware/arduino/avr/cores/arduino/USBDesc.h`
4. edit the following files and remove the shown lines:
    1. `arduino-x.x.x_LUFA/hardware/arduino/avr/cores/arduino/Arduino.h`
        * 233: `#include "USBAPI.h"`
        * 234: `#if defined(HAVE_HWSERIAL0) && defined(HAVE_CDCSERIAL)`
        * 235: `#error "Targets with both UART0 and CDC serial not supported"`
        * 236: `#endif`
    2. `arduino-x.x.x_LUFA/hardware/arduino/avr/cores/arduino/main.cpp`
        * 39: `#if defined(USBCON)`
        * 40: `USBDevice.attach();`
        * 41: `#endif`

That's it! You can now try start the Arduino IDE and compile the examples! :-)

[Arduino-Lufa]:https://github.com/Palatis/Arduino-Lufa

## Note
* By uploading the sketch to the board, you lose the ability to reset the board with setting-up 1200 baudrate, connect, then disconnect. This is used by the Arduino IDE to reset the board while uploading sketch. You can to manually reset the board by pressing the hardware reset button when the console prompts something similar to:

<code>Forcing reset using 1200bps open/close on port COM5    
PORTS {COM1, COM5, COM6, } / {COM1, COM5, COM6, } => {}    
PORTS {COM1, COM5, COM6, } / {COM1, COM5, COM6, } => {}    
PORTS {COM1, COM5, COM6, } / {COM1, COM5, COM6, } => {}    
...</code>

* If done correctly, the LED on pin 13 will being fading and you'll see the upload taking progress in the console.

## Credits
* Victor Tseng: palatis _AT_ gmail _DOT_ com (Original Author)
* Daniel Korgel (Contributor)
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
