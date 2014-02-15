#ifndef __LUFACDCSERIAL_H__
#define __LUFACDCSERIAL_H__

#include <LUFA.h>
#include <Stream.h>
#include <Print.h>

#if (RAMEND < 1000)
#define SERIAL_BUFFER_SIZE 16
#else
#define SERIAL_BUFFER_SIZE 64
#endif

class LUFACDCSerial : public Stream
{
public:
	LUFACDCSerial(USB_ClassInfo_CDC_Device_t* const);

	void begin(unsigned long);
	void begin(unsigned long, uint8_t);
	void end(void);

	virtual int available(void);
	virtual void accept(void);
	virtual int peek(void);
	virtual int read(void);
	virtual void flush(void);
	virtual size_t write(uint8_t);
	using Print::write; // pull in write(str) and write(buf, size) from Print
	operator bool();

private:
	USB_ClassInfo_CDC_Device_t* const _CDCInterfaceInfo;
	volatile uint8_t _rx_buffer_head;
	volatile uint8_t _rx_buffer_tail;
	unsigned char _rx_buffer[SERIAL_BUFFER_SIZE];
};

#endif