/*
 * Include this file in one of your project's c source file.
 * For example, create a file named "LUFA.c" and include this.
 * === LUFA.c ===
 * #include "LUFAConfig.h"
 * #include <LUFA.c.inc>
 * ==============
 */

#ifndef __LUFA_C__
#define __LUFA_C__

#define __INCLUDE_FROM_USB_DRIVER

#define __INCLUDE_FROM_DEVICESTDREQ_C
#define __INCLUDE_FROM_EVENTS_C
#define __INCLUDE_FROM_HOSTSTDREQ_C
#define __INCLUDE_FROM_USBTASK_C
#define __INCLUDE_FROM_USB_CONTROLLER_C

#include <LUFA/LUFA/Drivers/USB/Core/USBMode.h>

#if defined(USB_CAN_BE_DEVICE)
# define __INCLUDE_FROM_AUDIO_DEVICE_C
# define __INCLUDE_FROM_CDC_DEVICE_C
# define __INCLUDE_FROM_MASSSTORAGE_DEVICE_C
# define __INCLUDE_FROM_PRINTER_DEVICE_C
# define __INCLUDE_FROM_RNDIS_DEVICE_C
#endif

#if defined(USB_CAN_BE_HOST)
# define __INCLUDE_FROM_ANDROIDACCESSORY_HOST_C
# define __INCLUDE_FROM_AUDIO_HOST_C
# define __INCLUDE_FROM_CDC_HOST_C
# define __INCLUDE_FROM_HID_HOST_C
# define __INCLUDE_FROM_MASSSTORAGE_HOST_C
# define __INCLUDE_FROM_MIDI_HOST_C
# define __INCLUDE_FROM_PRINTER_HOST_C
# define __INCLUDE_FROM_RNDIS_HOST_C
# define __INCLUDE_FROM_STILLIMAGE_HOST_C
#endif

#include <LUFA/LUFA/Drivers/USB/USB.h>

#include <LUFA/LUFA/Drivers/USB/Core/ConfigDescriptors.c>
#include <LUFA/LUFA/Drivers/USB/Core/Events.c>
#include <LUFA/LUFA/Drivers/USB/Core/USBTask.c>
#include <LUFA/LUFA/Drivers/USB/Class/Common/HIDParser.c>

#if defined(USB_CAN_BE_DEVICE)
# include <LUFA/LUFA/Drivers/USB/Core/DeviceStandardReq.c>
# include <LUFA/LUFA/Drivers/USB/Class/Device/AudioClassDevice.c>
# include <LUFA/LUFA/Drivers/USB/Class/Device/CDCClassDevice.c>
# include <LUFA/LUFA/Drivers/USB/Class/Device/HIDClassDevice.c>
# include <LUFA/LUFA/Drivers/USB/Class/Device/MassStorageClassDevice.c>
# include <LUFA/LUFA/Drivers/USB/Class/Device/MIDIClassDevice.c>
# include <LUFA/LUFA/Drivers/USB/Class/Device/PrinterClassDevice.c>
# include <LUFA/LUFA/Drivers/USB/Class/Device/RNDISClassDevice.c>
#endif

#if defined(USB_CAN_BE_HOST)
# include <LUFA/LUFA/Drivers/USB/Core/HostStandardReq.c>
# include <LUFA/LUFA/Drivers/USB/Class/Host/AndroidAccessoryClassHost.c>
# include <LUFA/LUFA/Drivers/USB/Class/Host/AudioClassHost.c>
# include <LUFA/LUFA/Drivers/USB/Class/Host/CDCClassHost.c>
# include <LUFA/LUFA/Drivers/USB/Class/Host/HIDClassHost.c>
# include <LUFA/LUFA/Drivers/USB/Class/Host/MassStorageClassHost.c>
# include <LUFA/LUFA/Drivers/USB/Class/Host/MIDIClassHost.c>
# include <LUFA/LUFA/Drivers/USB/Class/Host/PrinterClassHost.c>
# include <LUFA/LUFA/Drivers/USB/Class/Host/RNDISClassHost.c>
# include <LUFA/LUFA/Drivers/USB/Class/Host/StillImageClassHost.c>
#endif

#if defined(USB_CAN_BE_BOTH)
# include <LUFA/LUFA/Drivers/USB/Core/OTG.c>
#endif

#if (ARCH == ARCH_AVR8)
# if defined(USB_CAN_BE_DEVICE)
# include<LUFA/LUFA/Drivers/USB/Core/AVR8/Device_AVR8.c>
#  include <LUFA/LUFA/Drivers/USB/Core/AVR8/Endpoint_AVR8.c>
#  include <LUFA/LUFA/Drivers/USB/Core/AVR8/EndpointStream_AVR8.c>
# endif
# if defined(USB_CAN_BE_HOST)
#  include <LUFA/LUFA/Drivers/USB/Core/AVR8/Host_AVR8.c>
#  include <LUFA/LUFA/Drivers/USB/Core/AVR8/Pipe_AVR8.c>
#  include <LUFA/LUFA/Drivers/USB/Core/AVR8/PipeStream_AVR8.c>
# endif
# if defined(USB_CAN_BE_BOTH)
#  include <LUFA/LUFA/Drivers/USB/Core/OTG_AVR8.c>
# endif
# include <LUFA/LUFA/Drivers/USB/Core/AVR8/USBController_AVR8.c>
# include <LUFA/LUFA/Drivers/USB/Core/AVR8/USBInterrupt_AVR8.c>
#elif (ARCH == ARCH_XMEGA)
# if defined(USB_CAN_BE_DEVICE)
#  include <LUFA/LUFA/Drivers/USB/Core/XMEGA/Device_XMEGA.c>
#  include <LUFA/LUFA/Drivers/USB/Core/XMEGA/Endpoint_XMEGA.c>
#  include <LUFA/LUFA/Drivers/USB/Core/XMEGA/EndpointStream_XMEGA.c>
# endif
# if defined(USB_CAN_BE_HOST)
#  include <LUFA/LUFA/Drivers/USB/Core/XMEGA/Host_XMEGA.c>
#  include <LUFA/LUFA/Drivers/USB/Core/XMEGA/Pipe_XMEGA.c>
#  include <LUFA/LUFA/Drivers/USB/Core/XMEGA/PipeStream_XMEGA.c>
# endif
# if defined(USB_CAN_BE_BOTH)
#  include <LUFA/LUFA/Drivers/USB/Core/OTG_XMEGA.c>
# endif
# include <LUFA/LUFA/Drivers/USB/Core/XMEGA/USBController_XMEGA.c>
# include <LUFA/LUFA/Drivers/USB/Core/XMEGA/USBInterrupt_XMEGA.c>
#elif (ARCH == ARCH_UC3)
# if defined(USB_CAN_BE_DEVICE)
#  include <LUFA/LUFA/Drivers/USB/Core/UC3/Device_UC3.c>
#  include <LUFA/LUFA/Drivers/USB/Core/UC3/Endpoint_UC3.c>
#  include <LUFA/LUFA/Drivers/USB/Core/UC3/EndpointStream_UC3.c>
# endif
# if defined(USB_CAN_BE_HOST)
#  include <LUFA/LUFA/Drivers/USB/Core/UC3/Host_UC3.c>
#  include <LUFA/LUFA/Drivers/USB/Core/UC3/Pipe_UC3.c>
#  include <LUFA/LUFA/Drivers/USB/Core/UC3/PipeStream_UC3.c>
# endif
# if defined(USB_CAN_BE_BOTH)
#  include <LUFA/LUFA/Drivers/USB/Core/OTG_UC3.c>
# endif
# include <LUFA/LUFA/Drivers/USB/Core/UC3/USBController_UC3.c>
# include <LUFA/LUFA/Drivers/USB/Core/UC3/USBInterrupt_UC3.c>
# include <LUFA/LUFA/Platform/UC3/InterruptManagement.c>
#endif

#endif