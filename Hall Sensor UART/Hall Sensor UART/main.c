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
//#define Mux0 6
#define Mux1 7
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
	
	DDRD &= ~(1<<Mux0);
	DDRD &= ~(1<<Mux1);
	DDRB &= ~(1<<Mux2);
	DDRB &= ~(1<<Mux3);
	DDRC &= ~(1<<Mux4);
	DDRC &= ~(1<<Mux5);
	DDRC &= ~(1<<Mux6);
	DDRC &= ~(1<<Mux7);
}

void SetABC(uint8_t row)
{
	PORTD &= ~(1<<A)&~(1<<B)&~(1<<C);if((row >> 2) & 1){PORTD |= (1<<C);}else if((row >> 1) & 1) {PORTD |= (1<<B);}else if((row >> 0) & 1) {PORTD |= (1<<A);}

// 	if((row >> 2) & 1) {
// 		PORTD |= (1<<C);
// 		} else {
// 		PORTD &= ~(1<<C);
// 	}
// 
// 	if((row >> 1) & 1) {
// 		PORTD |= (1<<B);
// 		} else {
// 		PORTD &= ~(1<<B);
// 	}
// 
// 	if((row >> 0) & 1) {
// 		PORTD |= (1<<A);
// 		} else {
// 		PORTD &= ~(1<<A);
// 	}

// 	switch (row)
// 	{
// 		case 0 :
// 		PORTC |= (1<<C)|(1<<B);
// 		PORTC &= ~(1<<A);
// 		break;
// 		case 1 :
// 		PORTC |= (1<<B);
// 		PORTC &= ~(1<<A) &~(1<<C);
// 		break;
// 		case 2 :
// 		PORTC |= (1<<C)|(1<<B);
// 		PORTC &= ~(1<<A);
// 		break;
// 		case 3 :
// 		PORTC &= ~(1<<A)&~(1<<B)&~(1<<C);
// 		break;
// 		case 4 :
// 		PORTC |= (1<<A);
// 		PORTC &= ~(1<<B)&~(1<<C);
// 		break;
// 		case 5 :
// 		PORTC |= (1<<C)|(1<<A);
// 		PORTC &= ~(1<<B);
// 		break;
// 		case 6 :
// 		PORTC |= (1<<A)|(1<<B);
// 		PORTC &= ~(1<<C);
// 		break;
// 		case 7 :
// 		PORTC |= (1<<A)|(1<<B)|(1<<C);
// 		break;
// 	}
//
}

uint8_t GatherMuxData(uint8_t Mux)
{
	if(Mux == 0) {
		Mux = Mux0;
	} else if(Mux == 1) {
		Mux = Mux1;
	} else if(Mux == 2) {
		Mux = Mux2;
	} else if(Mux == 3) {
		Mux = Mux3;
	} else if(Mux == 4) {
		Mux = Mux4;
	} else if(Mux == 5) {
		Mux = Mux5;
	} else if(Mux == 6) {
		Mux = Mux6;
	} else {
		Mux = Mux7;
	} 
	
	uint8_t MuxData = 0x00;
	for (uint8_t i = 0; i < 8; i++) {
		SetABC(i);
		PIND |= (1<<6);
		if(bit_is_clear(PIND,PD6)) {
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
	
	DDRB |= (1<<2); //SetLED as output
		
	//uint8_t UART_lastRecievedByte;
	USART_init();
    while (1) 
    {
		//UART_lastRecievedByte = USART_Receive();
		
		//PIND |= (1<<Mux0);
		
		//uint8_t MD0 = 0x00; //GatherMuxData(0);
		
		PIND |= (1<<6);
		
		SetABC(3);
		
		//PORTD &= ~(1<<C);
		//PORTD &= ~(1<<B);
		//PORTD &= ~(1<<A);
				
		if(bit_is_clear(PIND,Mux0)) {
		//if ((PIND & (1<<Mux0))) {
			PORTB |= (1<<2);
			//MD0 = 0xFF;
		} else {
			PORTB &= ~(1<<2);
		}
		
// 		PORTD |= (1<<C);
// 		
// 		//if(bit_is_clear(PIND,Mux0)) {
// 		if ((PIND & (1<<Mux0))) {
// 			MD0 |= (1<<1);
// 		}
// 		
// 		PORTD &= ~(1<<C);
// 		PORTD |= (1<<B);
// 		
// 		//if(bit_is_clear(PIND,Mux0)) {
// 		if ((PIND & (1<<Mux0))) {
// 			MD0 |= (1<<2);
// 		}
// 		
// 		PORTD |= (1<<C);
// 		
// 		//if(bit_is_clear(PIND,Mux0)) {
// 		if ((PIND & (1<<Mux0))) {
// 			MD0 |= (1<<3);
// 		}
// 		
// 		PORTD &= ~(1<<C);
// 		PORTD &= ~(1<<B);
// 		PORTD |= (1<<A);
// 		
// 		//if(bit_is_clear(PIND,Mux0)) {
// 		if ((PIND & (1<<Mux0))) {
// 			MD0 |= (1<<4);
// 		}
// 		
// 		PORTD |= (1<<C);
// 		
// 		//if(bit_is_clear(PIND,Mux0)) {
// 		if ((PIND & (1<<Mux0))) {
// 			MD0 |= (1<<5);
// 		}
// 		
// 		PORTD &= ~(1<<C);
// 		PORTD |= (1<<B);
// 		
// 		//if(bit_is_clear(PIND,Mux0)) {
// 		if ((PIND & (1<<Mux0))) {
// 			MD0 |= (1<<6);
// 		}
// 		
// 		PORTD |= (1<<C);
// 		
// 		//if(bit_is_clear(PIND,Mux0)) {
// 		if ((PIND & (1<<Mux0))) {
// 			MD0 |= (1<<7);
// 		}
		
		//Sending UART message 0xF0
		//USART_Transmit(MD0);
    }
}

