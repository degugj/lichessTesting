/*
 * EEPROM Functions.c
 *
 * Created: 3/6/2021 7:55:20 PM
 * Author : Samantha Klein
 * SDP 2021
 * code derived from embedds.com/programming-avr-i2c-interface/ and ATmega328 data sheet
 */ 


#include "ee24c16.h"


uint8_t EEWriteByte(uint16_t u16addr, uint8_t u8data)
{
	TWIStart();
	if(TWIGetStatus() != 0x08)
	return ERROR;
	// Select device and send A4 A1 A0 address bits
	TWIWrite((EEDEVADR) | (uint8_t) ((u16addr)>>7));
	if(TWIGetStatus() != 0x18)
	return ERROR;
	// Send the rest of address
	
}