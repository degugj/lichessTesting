/*
 * EEPROM Functions.c
 *
 * Created: 3/6/2021 7:55:20 PM
 * Author : Samantha Klein
 * SDP 2021
 * code derived from embedds.com/programming-avr-i2c-interface/ and ATmega328 data sheet
 */ 

#include "ee24c16.h"

uint8_t EEWriteByte(uint16_t u16addr, uint8_t u8data) // write byte to 24C16
{
	TWIStart();
	if(TWIGetStatus() != 0x08)
		return ERROR;
	// Select device and send A4 A1 A0 address bits
	TWIWrite((EEDEVADR) | (uint8_t) ((u16addr)>>7));
	if(TWIGetStatus() != 0x18)
		return ERROR;
	// Send the rest of address
	TWIWrite((uint8_t)(u16addr));
	if(TWIGetStatus() != 0x28)
		return ERROR;
	//write byte to eeprom
	TWIWrite(u8data);
	if(TWIGetStatus() != 0x28)
		return ERROR;
	TWIStop();
	return SUCCESS;
}

uint8_t EEWritePage(uint8_t page, uint8_t *u8data) // write byte to 24C16
{
	//calculate page address
	uint8_t u8paddr = 0;
	uint8_t i;
	u8paddr = page<<4;
	TWIStart();
	if (TWIGetStatus() != 0x08)
	return ERROR;
	//select page start address and send A2 A1 A0 bits send write command
	TWIWrite(((EEDEVADR)|(u8paddr>>3))&(~1));
	if (TWIGetStatus() != 0x18)
	return ERROR;
	//send the rest of address
	TWIWrite((u8paddr<<4));
	if (TWIGetStatus() != 0x28)
	return ERROR;
	//write page to eeprom
	for (i=0; i<16; i++)
	{
		TWIWrite(*u8data++);
		if (TWIGetStatus() != 0x28)
		return ERROR;
	}
	TWIStop();
	return SUCCESS;
}

uint8_t EEReadByte(uint16_t u16addr, uint8_t *u8data)
{
	//uint8_t databyte;
	TWIStart();
	if (TWIGetStatus() != 0x08)
	return ERROR;
	//select devise and send A2 A1 A0 address bits
	TWIWrite((EEDEVADR)|((uint8_t)((u16addr & 0x0700)>>7)));
	if (TWIGetStatus() != 0x18)
	return ERROR;
	//send the rest of address
	TWIWrite((uint8_t)(u16addr));
	if (TWIGetStatus() != 0x28)
	return ERROR;
	//send start
	TWIStart();
	if (TWIGetStatus() != 0x10)
	return ERROR;
	//select devise and send read bit
	TWIWrite((EEDEVADR)|((uint8_t)((u16addr & 0x0700)>>7))|1);
	if (TWIGetStatus() != 0x40)
	return ERROR;
	*u8data = TWIReadNACK();
	if (TWIGetStatus() != 0x58)
	return ERROR;
	TWIStop();
	return SUCCESS;
}

uint8_t EEReadPage(uint8_t page, uint8_t *u8data)
{
	//calculate page address
	uint8_t u8paddr = 0;
	uint8_t i;
	u8paddr = page<<4;
	TWIStart();
	if (TWIGetStatus() != 0x08)
	return ERROR;
	//select page start address and send A2 A1 A0 bits send write command
	TWIWrite(((EEDEVADR)|(u8paddr>>3))&(~1));
	if (TWIGetStatus() != 0x18)
	return ERROR;
	//send the rest of address
	TWIWrite((u8paddr<<4));
	if (TWIGetStatus() != 0x28)
	return ERROR;
	//send start
	TWIStart();
	if (TWIGetStatus() != 0x10)
	return ERROR;
	//select devise and send read bit
	TWIWrite(((EEDEVADR)|(u8paddr>>3))|1);
	if (TWIGetStatus() != 0x40)
	return ERROR;
	for (i=0; i<15; i++)
	{
		*u8data++ = TWIReadACK();
		if (TWIGetStatus() != 0x50)
		return ERROR;
	}
	*u8data = TWIReadNACK();
	if (TWIGetStatus() != 0x58)
	return ERROR;
	TWIStop();
	return SUCCESS;
}
