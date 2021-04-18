/*
 * Hall Sensor UART.c
 *
 * Created: 3/18/2021 3:20:48 PM
 * Author : Sam Klein
 */ 


#define F_CPU 16000000

#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#define A 0
#define B 7
#define C 6

#define Mux0 2
#define Mux1 3
#define Mux2 4
#define Mux3 5

#define Mux4 0
#define Mux5 1
#define Mux6 2
#define Mux7 3


uint8_t FSMode = 0;
uint8_t MD0;
uint8_t MD1;
uint8_t MD2;
uint8_t MD3;
uint8_t MD4;
uint8_t MD5;
uint8_t MD6;
uint8_t MD7;

uint8_t LD0;
uint8_t LD1;
uint8_t LD2;
uint8_t LD3;
uint8_t LD4;
uint8_t LD5;
uint8_t LD6;
uint8_t LD7;

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
	DDRB |= (1<<A);
	DDRD |= (1<<B);
	DDRD |= (1<<C);
	
	DDRD &= ~(1<<2);
	DDRD &= ~(1<<3);
	DDRD &= ~(1<<4);
	DDRD &= ~(1<<5);
	
	DDRC &= ~(1<<0);
	DDRC &= ~(1<<1);
	DDRC &= ~(1<<2);
	DDRC &= ~(1<<3);
}

void SetABC(uint8_t row)
{
 		PORTD &= ~(1<<B)&~(1<<C);
 		PORTB &= ~(1<<A);
 		
 		switch (row)
 		{
	 		
	 		case 0:
	 		PORTB |= (1<<A);
	 		PORTD |= (1<<B);
	 		PORTD &= ~(1<<C);
	 		break;
	 		
	 		case 1 :
	 		PORTD |= (1<<B);
	 		PORTD &= ~(1<<C);
	 		PORTB &= ~(1<<A);
	 		break;
	 		
	 		case 2 :
	 		PORTB |= (1<<A);
	 		PORTD &= ~(1<<B)&~(1<<C);
	 		break;
	 		
	 		case 3 :
	 		PORTD &= ~(1<<B)&~(1<<C);
	 		PORTB &= ~(1<<A);
	 		break;
	 		
	 		case 4 :
	 		PORTD |= (1<<C);
	 		PORTD &= ~(1<<B);
	 		PORTB &= ~(1<<A);
	 		break;
	 		
	 		
	 		case 5 :
	 		PORTD |= (1<<C);
	 		PORTD &= ~(1<<B);
	 		PORTB |= (1<<A);
	 		break;
	 		
	 		
	 		case 6 :
	 		PORTD |= (1<<C)|(1<<B);
	 		PORTB &= ~(1<<A);
	 		break;
	 		
	 		case 7 :
	 		PORTD |= (1<<B)|(1<<C);
	 		PORTB |= (1<<A);
	 		break;
 		}
 		//_delay_ms(5);


}




uint8_t GatherMuxDataC(uint8_t Mux)
{

	
	uint8_t MuxData = 0x00;
	
	for (uint8_t i = 0; i < 8; i++) {
		SetABC(i);
		//_delay_ms(500);
		if (!(PINC & (1<<Mux))){
			MuxData |= (1<<i);
		}
	}
	
	return MuxData;
	
}

uint8_t GatherMuxDataD(uint8_t Mux)
{

	
	uint8_t MuxData = 0x00;
	
	for (uint8_t i = 0; i < 8; i++) {
		SetABC(i);
		//_delay_ms(500);
		if (!(PIND & (1<<Mux))){
			MuxData |= (1<<i);
		}
	}
	
	return MuxData;
	
}

void SendData(uint8_t Byte1, uint8_t Byte2)
{
	USART_Transmit(Byte1);
	USART_Transmit(Byte2);
}



void DumpAllData(void) {
	
	MD7 = 0xFF;
	MD6 = 0xFF;
	MD5 = 0xFF;
	MD4 = 0xFF;
	MD3 = 0xFF;
	MD2 = 0xFF;
	MD1 = 0xFF;
	MD0 = 0xFF;
	
	MD7 = GatherMuxDataC(0);
	MD6 = GatherMuxDataC(1);
	MD5 = GatherMuxDataC(2);
	MD4 = GatherMuxDataC(3);
	MD3 = GatherMuxDataD(2);
	MD2 = GatherMuxDataD(3);
	MD1 = GatherMuxDataD(4);
	MD0 = GatherMuxDataD(5);

	
	SendData(0x00,MD0);
	SendData(0x01,MD1);
	SendData(0x02,MD2);
	SendData(0x03,MD3);
	SendData(0x04,MD4);
	SendData(0x05,MD5);
	SendData(0x06,MD6);
	SendData(0x07,MD7);
}

void FastScan(void) {
	
	LD0 = MD0;
	LD1 = MD1;
	LD2 = MD2;
	LD3 = MD3;
	LD4 = MD4;
	LD5 = MD5;
	LD6 = MD6;
	LD7 = MD7;
	
		MD7 = GatherMuxDataC(0);
		MD6 = GatherMuxDataC(1);
		MD5 = GatherMuxDataC(2);
		MD4 = GatherMuxDataC(3);
		MD3 = GatherMuxDataD(2);
		MD2 = GatherMuxDataD(3);
		MD1 = GatherMuxDataD(4);
		MD0 = GatherMuxDataD(5);
	

// 	if ((MD0 != LD0) | (MD1 != LD1)) {
// 		//_delay_ms(100);
// 		MD0 = GatherMuxDataD(0);
// 		MD1 = GatherMuxDataD(1);
// 		MD1 &= ~(1<<3);
// 		//MD2 = GatherMuxDataB(2);
		
		if((MD0 != LD0) | (MD1 != LD1)| (MD2 != LD2)| (MD3 != LD3)| (MD4 != LD4)| (MD5 != LD5)| (MD6 != LD6)| (MD7 != LD7)      ) {
			SendData(0x00,MD0);
			SendData(0x01,MD1);
			SendData(0x02,MD2);
			SendData(0x03,MD3);
			SendData(0x04,MD4);
			SendData(0x05,MD5);
			SendData(0x06,MD6);
			SendData(0x07,MD7);
			
			LD0 = MD0;
			LD1 = MD1;
			LD2 = MD2;
			LD3 = MD3;
			LD4 = MD4;
			LD5 = MD5;
			LD6 = MD6;
			LD7 = MD7;
		}		
		
	}


void USART_interrupt_ENA(void)
{
	
	UCSR0B |= (1<<RXCIE0);
	sei();
}

void USART_interrupt_DIS(void)
{
	
	UCSR0B &= ~(1<<RXCIE0);
	//DRD &= ~(1<<DDD0)
	cli();
}

/*
* Function Name : Interrupt for UART Receive Command
 * Description : If a command is received while microcontroller is busy, will transmit Gantry Busy Err Code
 * Input Parameters : None
 * Return value: None
 */
ISR(USART_RX_vect)
{
	uint8_t UART_Byte;
	UART_Byte = UDR0;
	
	if (UART_Byte == 0b00111000)
	{
		FSMode = 0; //none
	}
	
// 	else if (UART_Byte == 0b00101000)
// 	{
// 		FSMode = 1; //dump
// 	}
// 	else if (UART_Byte == 0b00110000)
// 	{
// 		FSMode = 2; //FS
// 	}
				
}

int main(void)
{
	FSMode = 0;
	
	MuxInit();
	uint8_t UART_lastRecievedByte;
	USART_init();
	USART_interrupt_ENA();
	
	while(1){	
		UART_lastRecievedByte = USART_Receive();
	
		if (UART_lastRecievedByte = 0b00101000) {
			DumpAllData();
			FSMode = 0;
		}
		if ( UART_lastRecievedByte = 0b00110000 )
		{
			while (FSMode == 2) {
				FastScan();
			}
			//FastScan();
		}
		
	

   }
}
