/*
 * twi.h
 *
 * Created: 1/7/2012 23:06:09
 *  Author: embedds.com
 */ 


#ifndef TWI_H_
#define TWI_H_
#include <avr/io.h>
void TWIInit(void);
void TWIStart(void);
void TWIStop(void);
void TWIWrite(uint8_t u8data);
uint8_t TWIReadACK(void);
uint8_t TWIReadNACK(void);
uint8_t TWIGetStatus(void);



#endif /* TWI_H_ */