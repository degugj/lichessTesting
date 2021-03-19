/*
 * Hall Sensor UART.c
 *
 * Created: 3/18/2021 3:20:48 PM
 * Author : Sam Klein
 */ 

#define F_CPU 16000000
#include <util/delay.h>
#include <avr/io.h>

// Mux0 = PD6
// Mux1 = PD7
// Mux2 = PB0
// Mux3 = PB1
// Mux4 = PC0
// Mux5 = PC1
// Mux6 = PC2
// Mux7 = PC3

// A = PD2
// B = PD3
// C = PD4

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
    //uint8_t UART_lastRecievedByte;
	USART_init();
    while (1) 
    {
		//UART_lastRecievedByte = USART_Receive();
		
		//Sending UART message 0xF0
		USART_Transmit(0xFF);
    }
}

