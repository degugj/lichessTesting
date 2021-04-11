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
		case 0:
 		PORTD |= (1<<A)|(1<<B);
 		PORTD &= ~(1<<C);
		break;
		case 7 :
		PORTD |= (1<<A)|(1<<B)|(1<<C);
		break;
	}
	_delay_ms(10);

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
			_delay_ms(250);
			if(bit_is_clear(PINB,Mux)) {
				MuxData |= (1<<i);
			}
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
			_delay_ms(250);
			if(bit_is_clear(PINC,Mux)) {
				MuxData |= (1<<i);
			}
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
			_delay_ms(250);
			if(bit_is_clear(PIND,Mux)) {
				MuxData |= (1<<i);
			}
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

void LEDon(void) {
	PORTB |= (1<<2);
}

void LEDoff(void) {
	PORTB &= ~(1<<2);
}

void DumpAllData(void) {
	//MD0 = GatherMuxDataD(0);
	MD0 = 0x00;
	MD1 = 0b01000000;
	//MD1 &= ~(1<<3);
	MD2 = GatherMuxDataB(2);
	//MD3 = GatherMuxDataB(3);
	MD3 = 0x00;
	//MD4 = GatherMuxDataC(4);
	MD4 = 0x00;
	//MD5 = GatherMuxDataC(5);
	MD5 = 0x00;
	MD6 = 0x00;
	//MD7 = GatherMuxDataC(7);
	MD7 = 0x00;
	
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
	//LD0 = MD0;
	//LD1 = MD1;
	LD2 = MD2;
	//LD3 = MD3;
	//LD4 = MD4;
	//LD5 = MD5;
	//LD6 = MD6;
	//LD7 = MD7;
	
	//MD0 = 0x00;
	//MD1 = 0b01000000;
	//MD1 &= ~(1<<3);
	MD2 = GatherMuxDataB(2);
	//MD3 = GatherMuxDataB(3);
	//MD3 = 0x00;
	//MD4 = GatherMuxDataC(4);
	//MD4 = 0x00;
	//MD5 = GatherMuxDataC(5);
	//MD5 = 0x00;
	//MD6 = 0x00;
	//MD7 = GatherMuxDataC(7);
	//MD7 = 0x00;
	
	if (MD2 != LD2) {
		SendData(0x00,MD0);
		SendData(0x01,MD1);
		SendData(0x02,MD2);
		SendData(0x03,MD3);
		SendData(0x04,MD4);
		SendData(0x05,MD5);
		SendData(0x06,MD6);
		SendData(0x07,MD7);
		
		//LD0 = MD0;
		//LD1 = MD1;
		LD2 = MD2;
		//LD3 = MD3;
		//LD4 = MD4;
		//LD5 = MD5;
		//LD6 = MD6;
		//LD7 = MD7;
		
	}
}

int main(void)
{
	MuxInit();
	uint8_t UART_lastRecievedByte;
	USART_init();
	
	while(1){	
		UART_lastRecievedByte = USART_Receive();
	
		if (UART_lastRecievedByte == 0b00101000) {
			DumpAllData();
		}
	
		UART_lastRecievedByte = USART_Receive();
	
		if (UART_lastRecievedByte == 0b00110000) {
			while (1) {
				FastScan();
				UART_lastRecievedByte = USART_Receive();
				if (UART_lastRecievedByte == 0b00111000) {
					break;
				}
			
			}
			//FastScan();
		}

   }
}
