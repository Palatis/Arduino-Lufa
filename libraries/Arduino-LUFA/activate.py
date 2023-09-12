#!/usr/bin/env python3
"""
Script to activate LUFA for Arduino.
When LUFA is active, Arduinos USB stack is deactivated and cannot be compiled against.

To deactivate LUFA and activate Arduinos USB stack, use the deactivate.py script.
"""

import textwrap
import fileinput
import re
import os
import shutil

# Get absolute paths
ARDUINO_LUFA_DIR = os.path.dirname(__file__)
ARDUINO_DIR = os.path.abspath(os.path.join(ARDUINO_LUFA_DIR, '../..'))

def absolute_path(path):
    """Converts path relative to ARDUINO_DIR to absolute one"""
    return os.path.abspath(os.path.join(ARDUINO_DIR, path))

#---------------------#
# File path constants #
#---------------------#

ARDUINO_HARDWARE_DIR = 'hardware/arduino'
ARDUINO_LUFA_HARDWARE_DIR = 'hardware/arduino-LUFA'
ARDUINO_CORE_DIR = 'hardware/arduino/avr/cores/arduino/'
ARDUINO_LUFA_CORE_DIR = 'hardware/arduino-LUFA/avr/cores/arduino/'
ARDUINO_LUFA_AVR_DIR = 'hardware/arduino-LUFA/avr'

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

#Text to be inserted above hidden sections in files
#Because the file might contain multi-line comments, #if 0 ... #endif are used
HIDE_HEADER = textwrap.dedent("""
    //=====================================
    //== This section is hidden by LUFA! ==
    //=====================================
    #if 0
""")

#Text to be inserted below hidden section in files
#This contains additional text to make sure it is easily found when deactivating LUFA
HIDE_FOOTER = textwrap.dedent("""
    END OF HIDDEN SECTION
    #endif
""")

#--------#
# Hiding #
#--------#
def hide_whole_file(path):
    """Hide whole file"""
    hide_section_in_file(path, False)

def unhide_whole_file(path):
    """Make previously hidden file available again"""
    unhide_section_in_file(path)

def hide_section_in_file(path, section):
    """
    Hide section
    If section is a falsey value, the whole file will be hidden
    """

    file_content = ""
    path = absolute_path(path)

    with open(path, 'r') as original:
        file_content = original.read()

    # Check if header or footer are already present
    if file_content.find(HIDE_HEADER) != -1 \
       or file_content.find(HIDE_HEADER) != -1:
        print(("INFO: Hide header and/or footer already present in file `{}'. "
               + 'File was left untouched.').format(path))
        return

    # Prepare insertion indices
    if section:
        section_length = len(section)
        section_start = file_content.find(section)
        if section_start == -1:
            print(("WARNING: Section below not found in file `{}`. "
                   + 'File was left untouched. Section:\n{}\n')
                  .format(path, section))
            return
    else:
        # Comment out whole file if section is falsey
        section_length = len(file_content)
        section_start = 0

    # Insert header before and footer after the section to hide
    modified_content = file_content[0 : section_start]                    \
                       + HIDE_HEADER                                      \
                       + file_content[section_start : section_start + section_length]\
                       + HIDE_FOOTER                                      \
                       + file_content[section_start + section_length : len(file_content)]\

    with open(path, 'w') as modified:
        modified.write(modified_content)

    # Report whether whole file or just a section has been hidden
    if not section:
        print("Successfully hid file `{}'!".format(path))
    else:
        print("Successfully hid section in file `{}'!".format(path))

def unhide_section_in_file(path):
    """Make previously hidden section available again"""

    file_content = ""
    path = absolute_path(path)

    with open(path, 'r') as original:
        file_content = original.read()

    header_start = file_content.find(HIDE_HEADER)
    footer_start = file_content.find(HIDE_FOOTER)

    # Check if header and footer were found
    if header_start == -1 or footer_start == -1:
        print(("WARNING: Hide header and/or footer not found in file `{}'. "
               + 'File was left untouched.').format(path))
        return

    # Check if header appears before footer
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
SUPPORTED_ARDUINO_IDE_VERSIONS = ['1.8.2', '1.8.3', '1.8.12', '1.8.13']

def get_arduino_ide_version():
    """Determine Arduino IDE version"""

    version_line = ""

    # Read changelog file. The first line always starts with 'ARDUINO X.Y.Z'
    with open(absolute_path('revisions.txt'), 'r') as revisions:
        version_line = revisions.readline()

    # Extract version number as string
    version_string = re.findall('[0-9].[0-9].[0-9][0-9]?', version_line)[0]

    return version_string

#----------------#
# Main functions #
#----------------#
def main_common(block_and_hide, folder):
    """Common functionality for activate and deactivate scripts"""

    arduino_ide_version = get_arduino_ide_version()

    if not arduino_ide_version in SUPPORTED_ARDUINO_IDE_VERSIONS:
        print(('WARNING: Arduino version {} has not been tested to be compatible.' \
               + "This script might not work properly.").format(arduino_ide_version))
    else:
        print('Compatible Arduino IDE version {} detected!' .format(arduino_ide_version))

    for file_to_block in FILES_TO_BLOCK:
        path = os.path.join(folder, file_to_block)
        if block_and_hide:
            hide_whole_file(path)
        else:
            unhide_whole_file(path)

    for in_file, section in SECTIONS_TO_HIDE_IN_FILES.items():
        path = os.path.join(folder, in_file)
        if block_and_hide:
            hide_section_in_file(path, section)
        else:
            unhide_section_in_file(path)

def copy_hardware_dir():
    shutil.copytree(absolute_path(ARDUINO_HARDWARE_DIR),absolute_path(ARDUINO_LUFA_HARDWARE_DIR))

def update_platform():
    myfile = fileinput.FileInput(absolute_path(os.path.join(ARDUINO_LUFA_AVR_DIR, "platform.txt")), inplace=True)

    for line in myfile:
        line = re.sub(r"name=(.*) AVR", r"name=\1 LUFA AVR", line.rstrip())
        print(line)

def update_boards():
    unsupported = []
    myfile = fileinput.FileInput(absolute_path(os.path.join(ARDUINO_LUFA_AVR_DIR, "boards.txt")), inplace=True)

    #first pass: append (LUFA) to names and check for unsupported boards
    for line in myfile:
        line = re.sub(r"name=(.*)", r"name=\1 (LUFA)", line.rstrip())

        if "build.mcu=" in line and not "atmega32u4" in line:
             unsup = line.split(".",1)[0]
             unsupported.append(unsup)
        print(line)

    #second pass: filter unsupported boards
    myfile = fileinput.FileInput(absolute_path(os.path.join(ARDUINO_LUFA_AVR_DIR, "boards.txt")), inplace=True)
    for line in myfile:
        if line.split(".",1)[0] in unsupported:
            line = "#" + line
            line = re.sub(r"LUFA", r"LUFA not supported", line.rstrip())
        print(line.rstrip())

def activate():
    """Activate function"""
    main_common(True, ARDUINO_CORE_DIR)

def deactivate():
    """Deactivate function"""
    main_common(False, ARDUINO_CORE_DIR)

def install():
    """Install function"""
    copy_hardware_dir()
    main_common(True, ARDUINO_LUFA_CORE_DIR)
    update_platform()
    update_boards()

def uninstall():
    """Uninstall function"""
    shutil.rmtree(absolute_path(ARDUINO_LUFA_HARDWARE_DIR))
 
if __name__ == '__main__':
    activate()
