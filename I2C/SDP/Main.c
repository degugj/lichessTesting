/*
 * Main.c
 *
 * Created: 2/22/2021 1:41:27 PM
 * Author : Samantha Klein
 * SDP 2021
 * code derived from embedds.com/programming-avr-i2c-interface/ and ATmega328 data sheet
 */ 

#include <avr/io.h>

#ifndef TWI_H_
#define TWI_H_
#define ERROR 1
#define SUCCESS (!ERROR)
#define EEDEVADR 0b10100000
#include <avr/io.h>
void TWIInit(void);
void TWIStart(void);
void TWIStop(void);
void TWIWrite(uint8_t u8data);
uint8_t TWIReadACK(void);
uint8_t TWIReadNACK(void);
uint8_t TWIGetStatus(void);

#endif



void TWIInit(void) // initialize TWI
{
	// set SCL to 400kHz
	TWSR = 0x00;
	TWBR = 0x0C;
	// enable TWI
	TWCR = (1<<TWEN);
}

void TWIStart(void)
{
	TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN);
	while (!(TWCR & (1<<TWINT)));
	
}

void TWIStop(void)
{
	TWCR = (1<<TWINT) | (1<<TWSTO) | (1<<TWEN);
}

void TWIWrite(uint8_t u8data)
{
	TWDR = u8data;
	TWCR = (1<<TWINT) | (1<<TWEN);
	while (!(TWCR & (1<<TWINT)));
}

uint8_t TWIReadACK(void)
{
	TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWEA);
	while (!(TWCR & (1<<TWINT)));
	return TWDR;
}

uint8_t TWIReadNACK(void)
{
	TWCR = (1<<TWINT) | (1<<TWEN);
	while (!(TWCR & (1<<TWINT)));
	return TWDR;
}

uint8_t TWIGetStatus(void)
{
	uint8_t status;
	// mast status;
	status = TWSR;
	return status;
}

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

int main(void)
{
	TWIInit();
	while(1) 
	{
		EEWriteByte(0x0F,0x0F);
		
	}
	
}