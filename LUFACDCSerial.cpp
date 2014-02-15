#include "LUFACDCSerial.h"

LUFACDCSerial::LUFACDCSerial(USB_ClassInfo_CDC_Device_t* const CDCInterfaceInfo):
	_CDCInterfaceInfo(CDCInterfaceInfo)
{
}

void LUFACDCSerial::begin(unsigned long)
{
}

void LUFACDCSerial::begin(unsigned long, uint8_t)
{
}

void LUFACDCSerial::end(void)
{
}

int LUFACDCSerial::available(void)
{
	return (unsigned int)(SERIAL_BUFFER_SIZE + _rx_buffer_head - _rx_buffer_tail) % SERIAL_BUFFER_SIZE;
}

void LUFACDCSerial::accept(void)
{
	int i = (unsigned int)(_rx_buffer_head+1) % SERIAL_BUFFER_SIZE;
	
	// if we should be storing the received character into the location
	// just before the tail (meaning that the head would advance to the
	// current location of the tail), we're about to overflow the buffer
	// and so we don't write the character or advance the head.

	// while we have room to store a byte
	while (i != _rx_buffer_tail) {
		int c = CDC_Device_ReceiveByte(_CDCInterfaceInfo);
		if (c == -1)
			break;	// no more data
		_rx_buffer[_rx_buffer_head] = c;
		_rx_buffer_head = i;

		i = (unsigned int)(_rx_buffer_head+1) % SERIAL_BUFFER_SIZE;
	}
}

int LUFACDCSerial::peek(void)
{
	if (_rx_buffer_head == _rx_buffer_tail) {
		return -1;
	} else {
		return _rx_buffer[_rx_buffer_tail];
	}
}

int LUFACDCSerial::read(void)
{
	// if the head isn't ahead of the tail, we don't have any characters
	if (_rx_buffer_head == _rx_buffer_tail) {
		return -1;
	} else {
		unsigned char c = _rx_buffer[_rx_buffer_tail];
		_rx_buffer_tail = (unsigned int)(_rx_buffer_tail + 1) % SERIAL_BUFFER_SIZE;
		return c;
	}
}

void LUFACDCSerial::flush(void)
{
	CDC_Device_Flush(_CDCInterfaceInfo);
}

size_t LUFACDCSerial::write(uint8_t data)
{
	/* only try to send bytes if the high-level CDC connection itself 
	 is open (not just the pipe) - the OS should set lineState when the port
	 is opened and clear lineState when the port is closed.
	 bytes sent before the user opens the connection or after
	 the connection is closed are lost - just like with a UART. */
	
	// TODO - ZE - check behavior on different OSes and test what happens if an
	// open connection isn't broken cleanly (cable is yanked out, host dies
	// or locks up, or host virtual serial port hangs)
	if (_CDCInterfaceInfo->State.ControlLineStates.HostToDevice > 0) {
		uint8_t r = CDC_Device_SendByte(_CDCInterfaceInfo, data);
		if (r == ENDPOINT_READYWAIT_NoError) {
			return r;
		} else {
			setWriteError();
			return 0;
		}
	}
	setWriteError();
	return 0;
}

// This operator is a convenient way for a sketch to check whether the
// port has actually been configured and opened by the host (as opposed
// to just being connected to the host).  It can be used, for example, in 
// setup() before printing to ensure that an application on the host is
// actually ready to receive and display the data.
// We add a short delay before returning to fix a bug observed by Federico
// where the port is configured (lineState != 0) but not quite opened.
LUFACDCSerial::operator bool() {
	bool result = _CDCInterfaceInfo->State.ControlLineStates.HostToDevice > 0;
	delay(10);
	return result;
}
