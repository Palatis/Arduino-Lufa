#!python3
"""
Script to activate LUFA for Arduino.
When LUFA is active, Arduinos USB stack is deactivated and cannot be compiled against.

To deactivate LUFA and activate Arduinos USB stack, use the deactivate.py script.
"""

import textwrap
import re

#---------------------#
# File path constants #
#---------------------#

ARDUINO_CORE_DIR = '../../hardware/arduino/avr/cores/arduino/'

FILES_TO_BLOCK = [
    'CDC.cpp',
    'PluggableUSB.cpp',
    'PluggableUSB.h',
    'USBAPI.h',
    'USBCore.cpp',
    'USBCore.h',
    'USBDesc.h'
]

SECTIONS_TO_HIDE_IN_FILES = {
    'Arduino.h' :
        textwrap.dedent("""
            #include "USBAPI.h"
            #if defined(HAVE_HWSERIAL0) && defined(HAVE_CDCSERIAL)
            #error "Targets with both UART0 and CDC serial not supported"
            #endif
        """),

    'main.cpp' :
        textwrap.dedent("""
            #if defined(USBCON)
            \tUSBDevice.attach();
            #endif
        """)
}

#Text to be inserted at the top of blocked files
BLOCK_HEADER = textwrap.dedent("""
    //==========================================================
    //== This file is blocked by LUFA and cannot be included! ==
    //==========================================================
    #error "LUFA is still activated! Please run `libraries/LUFA/deactivate.py' first!"
""")

#Text to be inserted above hidden sections in files
HIDE_HEADER = textwrap.dedent("""
    //=====================================
    //== This section is hidden by LUFA! ==
    //=====================================
    /*
""")

#Text to be inserted below hidden section in files
#This contains additional text to make sure it is easily found when deactivating LUFA
HIDE_FOOTER = textwrap.dedent("""
    END OF HIDDEN SECTION
    */
""")

#----------#
# Blocking #
#----------#
def block_file(path):
    """Prevent file from being included"""

    file_content = ""

    with open(path, 'r') as original:
        file_content = original.read()

    # Check if there already is a bloc header
    if file_content.find(BLOCK_HEADER) != -1:
        print(("INFO: Block header already present in file `{}'. "
               + 'File was left untouched.').format(path))
        return

    # Prepend block header
    with open(path, 'w') as blocked:
        blocked.write(BLOCK_HEADER + file_content)

    print("Successfully blocked file `{}'!".format(path))

def unblock_file(path):
    """Allow previously blocked file to be included again"""

    file_content = ""

    with open(path, 'r') as original:
        file_content = original.read()

    block_header_start = file_content.find(BLOCK_HEADER)
    if block_header_start == -1:
        print(("WARNING: Block header not found in file `{}'. "
               + 'File was left untouched.').format(path))
        return

    # Remove block header
    cropped_content = file_content[0 : block_header_start] \
        + file_content[block_header_start + len(BLOCK_HEADER) : len(file_content)]

    with open(path, 'w') as unblocked:
        unblocked.write(cropped_content)

    print("Successfully unblocked file `{}'!".format(path))

#--------#
# Hiding #
#--------#
def hide_section_in_file(path, section):
    """Hide section by surrounding it with comment tags"""

    file_content = ""

    with open(path, 'r') as original:
        file_content = original.read()

    section_start = file_content.find(section)
    if section_start == -1:
        print(("WARNING: Section below not found in file `{}`. "
               + 'File was left untouched. Section:\n{}\n')
              .format(path, section))
        return

    # Check if header or footer are already present
    if file_content.find(HIDE_HEADER) != -1 \
       or file_content.find(HIDE_HEADER) != -1:
        print(("INFO: Hide header and/or footer already present in file `{}'. "
               + 'File was left untouched.').format(path))
        return

    # Insert header before and footer after the section to hide
    modified_content = file_content[0 : section_start]                    \
                       + HIDE_HEADER                                      \
                       + file_content[section_start : section_start + len(section)]\
                       + HIDE_FOOTER                                      \
                       + file_content[section_start + len(section) : len(file_content)]\

    with open(path, 'w') as modified:
        modified.write(modified_content)

    print("Successfully hid section in file `{}'!".format(path))

def unhide_section_in_file(path):
    """Make previously hidden section available again"""

    file_content = ""

    with open(path, 'r') as original:
        file_content = original.read()

    header_start = file_content.find(HIDE_HEADER)
    footer_start = file_content.find(HIDE_FOOTER)
    if header_start == -1 or footer_start == -1:
        print(("WARNING: Hide header and/or footer not found in file `{}'. "
               + 'File was left untouched.').format(path))
        return

    if header_start > footer_start:
        print(("WARNING: Hide footer found before header in file `{}'. "
               + 'File was left untouched, it requires manual attention!')
              .format(path))
        return

    # Remove header and footer
    modified_content = file_content[0 : header_start]                                   \
                       + file_content[header_start + len(HIDE_HEADER) : footer_start]   \
                       + file_content[footer_start + len(HIDE_FOOTER) : len(file_content)]

    with open(path, 'w') as modified:
        modified.write(modified_content)

    print("Successfully unhid section in file `{}'!".format(path))

#--------------------------#
# Arudino version checking #
#--------------------------#
SUPPORTED_ARDUINO_IDE_VERSIONS = ['1.8.2', '1.8.3']

def get_arduino_ide_version():
    """Determine Arduino IDE version"""

    version_line = ""

    # Read changelog file. The first line always starts with 'ARDUINO X.Y.Z'
    with open('../../revisions.txt', 'r') as revisions:
        version_line = revisions.readline()

    # Extract version number as string
    version_string = re.findall('[0-9].[0-9].[0-9]', version_line)[0]

    return version_string

#----------------#
# Main functions #
#----------------#
def main_common(block_and_hide):
    """Common functionality for activate and deactivate scripts"""

    arduino_ide_version = get_arduino_ide_version()

    if not arduino_ide_version in SUPPORTED_ARDUINO_IDE_VERSIONS:
        print(('WARNING: Arduino version {} has not been tested to be compatible.' \
               + "This script might not work properly.").format(arduino_ide_version))
    else:
        print('Compatible Arduino IDE version {} detected!' .format(arduino_ide_version))

    for file_to_block in FILES_TO_BLOCK:
        path = ARDUINO_CORE_DIR + file_to_block
        if block_and_hide:
            block_file(path)
        else:
            unblock_file(path)

    for in_file, section in SECTIONS_TO_HIDE_IN_FILES.items():
        path = ARDUINO_CORE_DIR + in_file
        if block_and_hide:
            hide_section_in_file(path, section)
        else:
            unhide_section_in_file(path)

def activate():
    """Activate function"""
    main_common(True)

def deactivate():
    """Deactivate function"""
    main_common(False)

if __name__ == '__main__':
    activate()
