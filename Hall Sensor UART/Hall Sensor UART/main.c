/*
 * Hall Sensor UART.c
 *
 * Created: 3/18/2021 3:20:48 PM
 * Author : Sam Klein
 */ 


#define F_CPU 16000000

#include <util/delay.h>
#include <avr/io.h>

#define Mux0 PD6
#define Mux1 PD7
#define Mux2 PB0
#define Mux3 PB1
#define Mux4 PC0
#define Mux5 PC1
#define Mux6 PC2
#define Mux7 PC3

#define A PD2
#define B PD3
#define C PD4

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

int main(void)
{
    
	//PORTD = (1<<A) | (1<<B) | (1<<C); // Set A, B, C to high for now (Hall7 will be read)
	
	DDRD |= (1<<A);
	DDRD |= (1<<B);
	DDRD |= (1<<C);
	
	DDRD |= (0<<Mux0);
	DDRD |= (0<<Mux1);
	DDRB |= (0<<Mux2);
	DDRB |= (0<<Mux3);
	DDRC |= (0<<Mux4);
	DDRC |= (0<<Mux5);
	DDRC |= (0<<Mux6);
	DDRC |= (0<<Mux7);
	
	PORTD |= (1<<A);
	PORTD |= (1<<B);
	PORTD |= (1<<C);
	
	
	
	//uint8_t UART_lastRecievedByte;
	USART_init();
    while (1) 
    {
		//UART_lastRecievedByte = USART_Receive();
		
		//Sending UART message 0xF0
		USART_Transmit(0xFF);
    }
}

