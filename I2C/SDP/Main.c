/*
 * Main.c
 *
 * Created: 2/22/2021 1:41:27 PM
 * Author : Samantha Klein
 * SDP 2021
 * code derived from embedds.com/programming-avr-i2c-interface/ and ATmega328 data sheet and Peter Fleury's code
 */ 

#ifndef TWI_H_
#define TWI_H_
// #define ERROR 1
// #define SUCCESS (!ERROR)
#define EEDEVADR 0b10100000
#define F_CPU 4000000UL
#define SCL_CLOCK 100000L
#define TWI_READ 1
#define TWI_WRITE 0
#include <util/twi.h>
#include <avr/io.h>
#include <inttypes.h>
void TWIInit(void);
int TWIStart(void);
void TWIStop(void);
int TWIWriteAddress(uint8_t u8addr);
int TWIWrite(uint8_t u8data);
uint8_t TWIReadACK(void);
uint8_t TWIReadNACK(void);
uint8_t TWIGetStatus(void);

#endif


void TWIInit(void) // initialize TWI
{
	// set SCL to 400kHz
	TWSR = 0;
	TWBR = ((F_CPU/SCL_CLOCK) - 16)/2;
	// enable TWI
	TWCR = (1<<TWEN);
	
}

int TWIStart(void)
{
	TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN);
	while (!(TWCR & (1<<TWINT)));
	uint8_t twst;
	twst = TW_STATUS & 0xF8;
	if((twst != TW_START) && (twst != TW_REP_START) ) return 1;
	return 0;
}

void TWIStop(void)
{
	TWCR = (1<<TWINT) | (1<<TWSTO) | (1<<TWEN);
	while(TWCR & (1<<TWSTO));
}

int TWIWriteAddress(uint8_t u8addr) 
{
	TWDR = u8addr;
	TWCR = (1<<TWINT) | (1<<TWEN);
	while (!(TWCR & (1<<TWINT)));
	uint8_t twst;
	twst = TW_STATUS & 0xF8;
	if((twst != TW_MT_SLA_ACK) && (twst != TW_MR_SLA_ACK)) return 1;
	return 0;
}


int TWIWrite(uint8_t u8data)
{
	uint8_t twst;
	TWDR = u8data;
	TWCR = (1<<TWINT) | (1<<TWEN);
	while (!(TWCR & (1<<TWINT)));
	twst = TW_STATUS & 0xF8;
	if( twst != TW_MT_DATA_ACK) return 1;
	return 0;
	
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

uint8_t EEWriteByte(uint8_t u8addr, uint8_t u8data)
{
	TWIStart();
	if(TWIGetStatus() != 0x08)
	return 1;
	// Select device and send A4 A1 A0 address bits
	TWIWriteAddress(u8addr);
	if(TWIGetStatus() != 0x18)
	return 1;
	// Send the rest of address
	//TWIWrite((uint8_t)(u16addr));
	//if(TWIGetStatus() != 0x28)
	//return ERROR;
	//write byte to eeprom
	TWIWrite(u8data);
 	if(TWIGetStatus() != 0x28)
 	return 1;
	TWIStop();
	return 0;
}

int main(void)
{
	TWIInit();
	while(1)
	{
		EEWriteByte(0x0F,0x0F);
	}
	
}