/*
 * Hall Sensor UART.c
 *
 * Created: 3/18/2021 3:20:48 PM
 * Author : Sam Klein
 */ 


#define F_CPU 16000000

#include <util/delay.h>
#include <avr/io.h>

#define Mux0 6
#define Mux1 7
// #define Mux0 5 // register c
// #define Mux1 4 // register c
#define Mux2 0
#define Mux3 1
#define Mux4 0
#define Mux5 1
#define Mux6 2
#define Mux7 3

#define A 2
#define B 3
#define C 4

#define LED 2

void USART_Transmit(uint8_t data)
{

	_delay_ms(1);
	/* Wait for empty transmit buffer */
	while ( !( UCSR0A & (1<<UDRE0)) );
	/* Put data into buffer, sends the data */
	UDR0 = data;
}

/*
* Function Name : USART_Receive
 * Description: Returns the received parameters from UART
 * Input Parameters : NONE
 * Return value: 8-bit data received from UART
 */
int USART_Receive(void){
	while ( !(UCSR0A & (1<<RXC0)) ){}
	/* Get and return received data from buffer */
	return UDR0;
	
}

void USART_init(void){
	
	//DISABLE POWER REDUCTION FOR USART
	PRR &= ~( 1 << PRUSART0);
	/*Set baud rate */
	//9600 for 16MHz clock
	UBRR0L = 0b01100111;
	
	/*Enable receiver and transmitter //and Receive INterrupt*/
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);//|(1<<RXCIE0);
	/* 8-bit data */
	UCSR0C = (3<<UCSZ00);
}

void MuxInit(void) 
{
	DDRD |= (1<<A);
	DDRD |= (1<<B);
	DDRD |= (1<<C);
	
	DDRC &= ~(1<<Mux0);
	DDRC &= ~(1<<Mux1);
	DDRB &= ~(1<<Mux2);
	DDRB &= ~(1<<Mux3);
	DDRC &= ~(1<<Mux4);
	DDRC &= ~(1<<Mux5);
	DDRC &= ~(1<<Mux6);
	DDRC &= ~(1<<Mux7);
}

void SetABC(uint8_t row)
{
 	switch (row)
 	{
 		case 6 :
 		PORTD |= (1<<C)|(1<<B);
 		PORTD &= ~(1<<A);
 		break;
 		case 1 :
 		PORTD |= (1<<B);
 		PORTD &= ~(1<<A) &~(1<<C);
 		break;
 		case 4 :
 		PORTD |= (1<<C);
 		PORTD &= ~(1<<A)&~(1<<B);
 		break;
		case 3 :
		PORTD &= ~(1<<A)&~(1<<B)&~(1<<C);
 		break;
 		case 2 :
 		PORTD |= (1<<A);
 		PORTD &= ~(1<<B)&~(1<<C);
 		break;
 		case 5 :
 		PORTD |= (1<<C)|(1<<A);
 		PORTD &= ~(1<<B);
 		break;
 		case 0 :
 		PORTD |= (1<<A)|(1<<B);
 		PORTD &= ~(1<<C);
		break;
		case 7 :
		PORTD |= (1<<A)|(1<<B)|(1<<C);
		break;
	}

}

uint8_t GatherMuxDataB(uint8_t Mux)
{
	if(Mux == 2) {
		Mux = Mux2;
	} else {
		Mux = Mux3;
	} 
	
	uint8_t MuxData = 0x00;
	for (uint8_t i = 0; i < 8; i++) {
		SetABC(i);
		PINB |= (1<<6);
		if(bit_is_clear(PINB,Mux)) {
			MuxData |= (1<<i);
			//USART_Transmit(0xFF);
		}
	}
	return MuxData;
}

uint8_t GatherMuxDataC(uint8_t Mux)
{
	if(Mux == 4) {
		Mux = Mux4;
	} else if (Mux == 5) {
		Mux = Mux5;
	} else if (Mux == 6) {
		Mux = Mux6 ;
	} else {
		Mux = Mux7;
	}
	
	uint8_t MuxData = 0x00;
	for (uint8_t i = 0; i < 8; i++) {
		SetABC(i);
		PINC |= (1<<6);
		if(bit_is_clear(PINC,Mux)) {
			MuxData |= (1<<i);
			//USART_Transmit(0xFF);
		}
	}
	return MuxData;
}

uint8_t GatherMuxDataD(uint8_t Mux)
{
	if(Mux == 0) {
		Mux = Mux0;
	} else {
		Mux = Mux1;
	}
	
	uint8_t MuxData = 0x00;
	for (uint8_t i = 0; i < 8; i++) {
		SetABC(i);
		PIND |= (1<<6);
		if(bit_is_clear(PIND,Mux)) {
			MuxData |= (1<<i);
			//USART_Transmit(0xFF);
		}
	}
	return MuxData;
}

void SendData(uint8_t Byte1, uint8_t Byte2)
{
	USART_Transmit(Byte1);
	USART_Transmit(Byte2);
}

int main(void)
{
	
	MuxInit();
	
	//DDRB |= (1<<2); //SetLED as output
		
	uint8_t UART_lastRecievedByte;
	USART_init();
	
	uint8_t MD0;
	uint8_t MD1;
	uint8_t MD2;
	uint8_t MD3;
	uint8_t MD4;
	uint8_t MD5;
	uint8_t MD6;
	uint8_t MD7;
	
    while (1) 
    {
		MD0 = GatherMuxDataD(0);
		MD1 = GatherMuxDataD(1);
		MD2 = GatherMuxDataB(2);
		MD3 = GatherMuxDataB(3);
		MD4 = GatherMuxDataC(4);
		MD5 = 0x00;
		MD6 = GatherMuxDataC(6);
		MD7 = GatherMuxDataC(7);
		
		UART_lastRecievedByte = USART_Receive();
		
		if (UART_lastRecievedByte == 0b00101000) {
			SendData(0x00,MD0);
			SendData(0x01,MD1);
			SendData(0x02,MD2);
			SendData(0x03,MD3);
			SendData(0x04,MD4);
			SendData(0x05,MD5);
			SendData(0x06,MD6);
			SendData(0x07,MD7);
		}
		
// 		UART_lastRecievedByte = USART_Receive();
// 		
// 		if (UART_lastRecievedByte == 0b00110000) {
// 			SendData(0x00,MD0);
// 			SendData(0x01,MD1);
// 			SendData(0x02,MD2);
// 			SendData(0x03,MD3);
// 			SendData(0x04,MD4);
// 			SendData(0x05,MD5);
// 			SendData(0x06,MD6);
// 			SendData(0x07,MD7);
// 		}
// 		
		//PIND |= (1<<Mux0);
		
		//uint8_t MD0 = 0x00; //GatherMuxData(0);
		
		//SetABC(6);
				
// 		if(bit_is_clear(PIND,Mux0)) {
// 		//if ((PIND & (1<<Mux0))) {.
// 			PORTB |= (1<<2);
// 			//MD0 = 0xFF;
// 		} else {
// 			PORTB &= ~(1<<2);
// 		}
		
		//Sending UART message 0xF0
		//USART_Transmit(MD0);
    }
}

