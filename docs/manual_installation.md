# Manual Installation Instructions

Manual installation is somewhat tricky, because the stock USB stack is in the arduino core directory instead of a seperated library directory, so you cannot simply drop [Arduino-Lufa] to the library folder under your Sketchbook directory.

    The following setup was last tested with arduino-1.8.3 and LUFA 170418 
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

[LUFA]:http://www.fourwalledcubicle.com/LUFA.php
[Arduino-Lufa]:https://github.com/Palatis/Arduino-Lufa
