/*
 * usart.h
 *
 * Created: 1/7/2012 23:03:24
 *  Author: embedds.com
 */ 


#ifndef USART_H_
#define USART_H_
#include <stdio.h>
#include <avr/io.h>
#define USART_BAUDRATE 9600
#define UBRR_VALUE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1) 

void USART0Init(void);
int USART0SendByte(char u8Data, FILE *stream);
int USART0ReceiveByte(FILE *stream);



#endif /* USART_H_ */