/*
 * Main.c
 *
 * Created: 2/22/2021 1:41:27 PM
 * Author : Samantha Klein
 * SDP 2021
 * code derived from embedds.com/programming-avr-i2c-interface/ and ATmega328 data sheet
 */ 

#include <stdio.h>
#include <avr/io.h>
#include <avr/pgmspace.h>
#include "usart.h"
#include "ee24c16.h"

//set stream pointer
FILE usart0_str = FDEV_SETUP_STREAM(USART0SendByte, USART0ReceiveByte, _FDEV_SETUP_RW);
int main(void)
{
	uint8_t u8ebyte;
	uint8_t u8erbyte;
	uint16_t u16eaddress = 0x07F0;
	uint8_t page = 5;
	uint8_t i;
	uint8_t eereadpage[16];
	uint8_t eewritepage[16] = { 10, 44, 255, 46, 80, 87, 43, 130,
	210, 23, 1, 58, 46, 150, 12, 46 };
	//Initialize USART0
	USART0Init();
	//
	TWIInit();
	//assign our stream to standard I/O streams
	stdin=stdout=&usart0_str;
	printf("\nWrite byte %#04x to eeprom address %#04x", 0x58, u16eaddress);
	if (EEWriteByte(u16eaddress, 0x58) != ERROR)
	{
		printf_P(PSTR("\nRead byte From eeprom"));
		if (EEReadByte(u16eaddress, &u8ebyte) != ERROR)
		{
			printf("\n*%#04x = %#04x", u16eaddress, u8ebyte);
		}
		else printf_P(PSTR("\nStatus fail!"));

	}
	else printf_P(PSTR("\nStatus fail!"));
	
	printf_P(PSTR("\nWriting 16 bytes to page 5 "));
	if(EEWritePage(page, eewritepage) != ERROR)
	{
		printf_P(PSTR("\nReading 16 bytes from page 5 "));
		if (EEReadPage(page, eereadpage) != ERROR)
		{
			//compare send and read buffers
			for (i=0; i<16; i++)
			{
				if (eereadpage[i] != eewritepage[i])
				{
					break;
				}
				else continue;
			}
			if (i==16)
			printf_P(PSTR("\nPage write and read success!"));
			else
			printf_P(PSTR("\nPage write and read fail!"));
		} else printf_P(PSTR("\nStatus fail!"));

	}else printf_P(PSTR("\nStatus fail!"));

	printf_P(PSTR("\nContinue testing EEPROM from terminal!"));
	while(1)
	{
		printf("\nEnter EEPROM address to write (MAX = %u): ", EEMAXADDR);
		scanf("%u",&u16eaddress);
		printf("Enter data to write to EEPROM at address %u: ", u16eaddress);
		scanf("%u",&u8ebyte);
		printf_P(PSTR("\nWriting..."));
		EEWriteByte(u16eaddress, u8ebyte);
		printf_P(PSTR("\nTesting..."));
		if (EEReadByte(u16eaddress, &u8erbyte) !=ERROR)
		{
			if (u8ebyte==u8erbyte)
			printf_P(PSTR("\nSuccess!"));
			else
			printf_P(PSTR("\nFail!"));
		}
		else printf_P(PSTR("\nStatus fail!"));

		//TODO:: Please write your application code
	}
}

