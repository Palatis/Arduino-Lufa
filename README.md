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

As LUFA requires changes to the Arduino core files, it is installed as custom boards.

In the Arduino IDE, go to `File > Preferences`, and in `Additional Boards Manager URLs` add the following entry : `https://github.com/Palatis/Arduino-Lufa/raw/master/package_arduino-lufa_index.json`

<img src="readme_assets/preferences.png" height="250"
alt="File > Preferences"
title="File > Preferences"
/>

Restart Arduino IDE, and you should be able to find `Arduino LUFA AVR Boards` in the `Tools > Board > Boards Manager`

<img src="readme_assets/board_manager.png" height="250"
alt="Tools > Board > Boards Manager"
title="Tools > Board > Boards Manager"
/>

Click on install, and `Arduino LUFA AVR Boards` should now appear as a submenu in `Tools > Board`

<img src="readme_assets/boards.png" height="250"
alt="Tools > Board"
title="Tools > Board"
/>

## Installation (legacy)

While not recommended, it is still possible to use the [legacy installation] method.

[legacy installation]:libraries/Arduino-LUFA/README.md

## First run and use

To test Arduino-Lufa, select your board type from the `Tools > Board > Arduino LUFA AVR Boards`, and open the `File > Examples > Exemple for this board > Arduino-LUFA > LUFA_DualVirtualSerial` example.
Click __Verify__. 
(**Note**: only atmega32u4 based boards are marked as compatible and will appear, if you 
are using another board which should be compatible please open an issue. Also see Note on __Upload__ below)

<img src="readme_assets/open_example.png" height="250"
alt="File -> Examples -> Examples for this board -> Arduino-LUFA -> LUFA_DualVirtualSerial"
title="File -> Examples -> Examples for this board -> Arduino-LUFA -> LUFA_DualVirtualSerial"
/>

To use Arduino-Lufa, select a LUFA board and add `#include <LUFA.h>` to your sketch header.

### Note on uploading the LUFA_DualVirtualSerial sketch

By uploading this sketch to the board, you will prevent the Arduino IDE from automatically reset the board before uploading another sketch. This is normally done by setting up a seial connection with 1200 baud, connecting, then disconnecting.

You can, however, manually reset the board by pressing the hardware reset button when the upload starts. To better see this, enable "Show verbose output during upload" in your preferences and wait until the IDE repatedly prompts something like this:

```
PORTS {COM1, COM5, COM6, } / {COM1, COM5, COM6, } => {}
```

If done correctly, the LED on pin 13 will begin flashing and you'll see the upload progressing in the console.

This is not permanent, however. To go back to the original state, upload a sketch compiled without Arduino-Lufa, as explained below.

## Deactivating Arduino-Lufa

If you need to compile sketches that use the Arduino Core USB Stack, you'll need to select the board type from
the `Tools > Board > Arduino AVR Boards` submenu.

Refer to [legacy installation] document if you previously installed using the legacy method and wish to deactivate Arduino-Lufa

## Credits
* Victor Tseng: palatis _AT_ gmail _DOT_ com (Original Author)
* Daniel Korgel (Contributor)
* Felix Uhl (Contributor)
* CrazyRedMachine (Contributor)
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
