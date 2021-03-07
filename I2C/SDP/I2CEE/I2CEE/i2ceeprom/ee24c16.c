/*
 * 24c16.c
 *
 * Created: 1/7/2012 23:19:00
 *  Author: embedds.com
 */ 
#include "ee24c16.h"
//write byte to 24C16
uint8_t EEWriteByte(uint16_t u16addr, uint8_t u8data)
{
	TWIStart();
	if (TWIGetStatus() != 0x08)
		return ERROR;
	//select devise and send A2 A1 A0 address bits
	TWIWrite((EEDEVADR)|(uint8_t)((u16addr & 0x0700)>>7));
	if (TWIGetStatus() != 0x18)
		return ERROR;	
	//send the rest of address
	TWIWrite((uint8_t)(u16addr));
	if (TWIGetStatus() != 0x28)
		return ERROR;
	//write byte to eeprom
	TWIWrite(u8data);
	if (TWIGetStatus() != 0x28)
		return ERROR;
	TWIStop();
	return SUCCESS;
}
//write byte to 24C16
uint8_t EEWritePage(uint8_t page, uint8_t *u8data)
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