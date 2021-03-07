/*
 * TWI Functions.c
 *
 * Created: 2/24/2021 11:06:20 PM
 * Author : Samantha Klein
 * SDP 2021
 * code derived from embedds.com/programming-avr-i2c-interface/ and ATmega328 data sheet
 */ 

/*
#include <stdio.h>
#include <avr/io.h>
#include <avr/pgmspace.h>
#include "usart.h"
#include "ee24c16.h"
*/

#include "I2CEE/I2CEE/i2ceeprom/i2ceeprom/twi.h"

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


/*
TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN); //send start
while (!(TWCR & (1<<TWINT))); //wait for TWINT flag
if((TWSR & 0xF8) ! = START) ERROR(); //check TWI status register
TWDR = SLA_W;
TWCR = (1<<TWINT) | (1<<TWEN);
while (!(TWCR & (1<<TWINT))); //wait for TWINT flag
if((TWSR & 0xF8) ! = MT_SLA_ACK) ERROR();
TWDR = DATA;
TWCR = (1<<TWINT) | (1<<TWEN);
while (!(TWCR & (1<<TWINT))); //wait for TWINT flag
if((TWSR & 0xF8) ! = MT_DATA_ACK) ERROR();
TWCR = (1<<TWINT) | (1<<TWSTO) | (1<<TWEN); //send stop
*/