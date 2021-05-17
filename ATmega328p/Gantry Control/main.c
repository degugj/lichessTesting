/*
 * GantryCode.c
 *
 * Created: 28-Dec-20 3:11:50 PM
 * Author : stkya
 */ 

#define F_CPU 16000000 //Clock Speed 16MHz
//#define F_CPU 20000000 //Clock Speed 20MHz
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <string.h>

#include "UART_SEND_COMMANDS.h"
#include "EM_Control.h"
#include "RC522_Config.h"


//Pins Declaration for DIRECTION & IO
//Stepper Motors PORT C
#define stepX 2
#define stepY 0
#define dirX  3
#define dirY  1
#define ENA   4


//Calibration Switch PORT D
#define calX_SW 3
#define calY_SW 2
//Electromagnet Control PORT D
#define ena_EM 7
#define in1_EM 6
#define in2_EM 5
//RFID SPI PORT B
#define SCK_RF  5
#define MISO_RF 4
#define MOSI_RF 3
#define SS_RF   2
#define RST_RF  1


#define steps_per_unitlength 2001.875	//Steps per Unit Length of 25mm
#define steps_to_Y_equals_16  1400	//Initial Steps from Calibration to Y = 16
#define steps_to_X_equals_0  7875	//Initial Steps from Calibration to X = 0


#define datatype unsigned int
#define setGantrySpeed  28 //period of timing

uint8_t currentXADDR, currentYADDR;
uint8_t newXADDR, newYADDR;
uint8_t UART_lastRecievedByte;
uint8_t overshootMode = 0;


int main(void){
	_delay_ms(1000);
	gantryIO_init();
	USART_init();
	SPI_init();
	//EM_ON();
	//_delay_ms(1000);
	calibrate();
	//currentYADDR = 0;
	//currentXADDR = 0;
	//GO(12,8);
	//EM_FLIP();
	//EM_ON();
	//_delay_ms(1500);
	
	//EM_OFF();
	/* Replace with your application code */
	while (1)
	{
		//USART_Receive();
		//USART_Transmit(0xAB);
		//_delay_ms(100);
		UART_lastRecievedByte = USART_Receive();
		UART_decode_Command(UART_lastRecievedByte);
		
		//USART_Transmit(UART_lastRecievedByte);
	}
	
}



/*
* Function Name : gantryIO_init
 * Description: Sets data pin directions for RFID/EM/StepperDriver/Switches
 * Input Parameters : None
 * Return value: None
 */
void gantryIO_init(void)
{
	//Set Output for stepper control
	DDRC |= (1<<dirX)|(1<<dirY)|(1<<stepX)|(1<<stepY) ;
	PORTC |= ( 1 <<ENA);
	
	//Set Output for electromagnet control
	DDRD |= (1<<ena_EM)|(1<<in1_EM)|(1<<in2_EM);
	EM_OFF();
	
	//Set Input for calibration switches
	DDRD &= ~(1<<calX_SW) &~(1<<calY_SW);
	//Pull up for calibration switches
	PORTD |=(1<<calX_SW)|(1<<calY_SW);
	
	//UART INPUT and Initialize Level Shifters
	PORTC  |= (1<<PORTC5);
	DDRD &= ~(1<<DDD0) &~(1<<DDD1);
	
	
	//Set Input/Output for RFID Reader
	DDRB |=  (1<<MOSI_RF)|(1<<SS_RF)|(1<<SCK_RF)|(1<<RST_RF);
	DDRB &= ~(1<<MISO_RF);		
}

/*
* Function Name : dirY_LOWs
 * Description: Sets Y stepper direction as LOW. (Moves down)
 * Input Parameters : NONE
 * Return value: NONE
 */
void dirY_LOW(void){
	//_delay_us(6);
	PORTC &= ~(1<<dirY);
	_delay_us(6);
}

/*
* Function Name : dirY_HIGH
 * Description: Sets Y stepper direction as HIGH. (Moves Up)
 * Input Parameters : NONE
 * Return value: NONE
 */
void dirY_HIGH(void){
	//_delay_us(6);
	PORTC |= (1<<dirY);
	_delay_us(6);
}

/*
* Function Name : dirX_LOW
 * Description: Sets Y stepper direction as LOW. (Moves left)
 * Input Parameters : NONE
 * Return value: NONE
 */
void dirX_LOW(void){
	//_delay_us(6);
	PORTC &= ~(1<<dirX);
	_delay_us(6);
}

/*
* Function Name : dirX_HIGH
 * Description: Sets Y stepper direction as HIGH. (Moves RIGHT)
 * Input Parameters : NONE
 * Return value: NONE
 */
void dirX_HIGH(void){
	//_delay_us(6);
	PORTC |= (1<<dirX);
	_delay_us(6);
}

/*
* Function Name : TIMER_ON
 * Description: Turns off timer. Prescaler 64. Regular Timer.
 * Input Parameters : NONE
 * Return value: NONE
 */
void TIMER_ON (void)
{
	
	//DISABLE POWER REDUCTION FOR TIMER
	PRR &= ~( 1 << PRTIM0);
	//Turns on Timer with 64 Prescaler set
	//DIV 64 Prescaler
	TCCR0B |= ( 1 << CS01)|(1<<CS00);
	
}

/*
* Function Name : TIMER_OFF
 * Description: Turns off timer.
 * Input Parameters : NONE
 * Return value: NONE
 */
void TIMER_OFF(void)
{
	//ENABLE POWER REDUCTION FOR TIMER
	PRR |= ( 1 << PRTIM0);
	
	//Turns off Timer
	TCCR0B = 0x00;
	TCCR0A = 0x00;
	TIMSK0 = 0x00;
}

/*
* Function Name : X_CAL_move_towards_SW
 * Description: Moves X axis Stepper right until it presses switch. 
 * Input Parameters : NONE
 * Return value: NONE
 */
void X_CAL_move_towards_SW(void)
{	
	dirX_LOW();
	
	//Check if the Switch is already pressed
	if ((PIND & (1<<calX_SW))){
		return;
	}
	
	//If not
	//Run Stepper until it toggles the Switch.
	else {
		TIMER_ON();
		while (!(PIND & (1<<calX_SW)))
		{
			if (TCNT0 == setGantrySpeed)
			{
				PORTC ^= (1 << stepX);
				TCNT0 = 0x00;		//RESET COUNTER
			}
		}
	}
	PORTC &= ~(1<<stepX);
	TIMER_OFF();
	return;
	
}

/*
* Function Name : Y_CAL_move_towards_SW
 * Description: Moves Y axis Stepper right until it presses switch. 
 * Input Parameters : NONE
 * Return value: NONE
 */
void Y_CAL_move_towards_SW(void)
{
	dirY_HIGH();
	
	//Check if the Switch is already pressed
	if ((PIND & (1<<calY_SW))){ 
		return 0;
	}
	
	//If not
	//Run Stepper until it toggles the Switch.
	else { 
		TIMER_ON();
		while (!(PIND & (1<<calY_SW)))
		{
			if (TCNT0 == setGantrySpeed)
			{
				PORTC ^= (1 << stepY);
				TCNT0 = 0x00;		//RESET COUNTER
			}
		}
		}
		PORTC &= ~(1<<stepY);
		TIMER_OFF();
		return 0;
}

/*
* Function Name : round_Decimal
 * Description: Rounds the floating input to the nearest whole number
 * Input Parameters : Floating point decimal
 * Return value: Rounded number. See "datatype" above.
 */
 datatype round_Decimal(float input)
 {
	 datatype answer;
	 answer = input;
	 if ((input - answer) > 0.5  )
	 {
		 answer++;
	 }
	 
	 return answer;
 }

/*
* Function Name : move_straightX
 * Description: Moves Gantry X Axis by "move_X_units" unit. (1 unit = 1/2 Cell = 25mm)
 * Input Parameters : No. of units/points to move
 * Return value: NONE
 */
void move_straightX (uint8_t move_X_units)
{	
	step_straightX(round_Decimal(move_X_units*steps_per_unitlength));
}

/*
* Function Name : step_straightX
 * Description: Moves Gantry X Axis by no. of steps. Creates pulses for PUL X.
 *			  : Gantry Starts Slow, Speeds up, and slows down until stops. 30 different speeds
 * Input Parameters : No. of steps to make for the stepper motor
 * Return value: NONE
 */
void step_straightX (datatype steps)
{
	
	if (steps > 50000)
	{
		//fatal_ERROR();
		return 0;
	}
	
	TIMER_ON();
	uint8_t i,speed;
	int ii;
	
	speed = setGantrySpeed + 31;
	i = 31;
	while(i > 1)
	{
		ii = steps - 200;
		while(steps > ii)
		{
			if (TCNT0 == speed)
			{
				PORTC |= (1<<stepX);
				TCNT0 = 0x00;									//RESET COUNTER
				steps--;
			}
			else if( TCNT0 == speed/2)
			{
				PORTC &= ~(1<<stepX);
			}
		
		
		}//End while steps ii
		
		speed = speed - 1;
		i--;		
	}//End while i
	
	

	while(steps > 6000){
		if (TCNT0 == setGantrySpeed)
		{
			PORTC |= (1<<stepX);
			TCNT0 = 0x00;									//RESET COUNTER
			steps--;
		}
		else if( TCNT0 == setGantrySpeed/2)
		{
			PORTC &= ~(1<<stepX);
		}
	}

	i = 31;
	ii = 6000;
	speed = setGantrySpeed;
	
	while(i > 1)
	{
		ii = ii - 200;
		if (ii < 0)
		{
			ii = 0;
		}
		while(steps > ii)
		{
			if (TCNT0 == speed)
			{
				PORTC |= (1<<stepX);
				TCNT0 = 0x00;									//RESET COUNTER
				steps--;
			}
			else if( TCNT0 == speed/2)
			{
				PORTC &= ~(1<<stepX);
			}
			
			
		}//End while steps ii
		

		speed = speed + 1;
		i--;
		
	}//End while i
	
	TIMER_OFF();
	_delay_us(10);
	PORTC &= ~(1<<stepX);
	
}

/*
* Function Name : move_straightY
 * Description: Moves Gantry Y Axis by "move_Y_units" unit. (1 unit = 1/2 Cell = 25mm)
 * Input Parameters : No. of units/points to move
 * Return value: NONE
 */
void move_straightY (uint8_t move_Y_units)
{	
	step_straightY(round_Decimal(move_Y_units*steps_per_unitlength));
}

/*
* Function Name : step_straightY
 * Description: Moves Gantry Y Axis by no. of steps. Creates pulses for PUL Y.
 *			  : Gantry Starts Slow, Speeds up, and slows down until stops. 2 different speeds
 * Input Parameters : No. of steps to make for the stepper motor
 * Return value: NONE
 */
void step_straightY (datatype steps)
{
	if (steps > 33000)
	{
		//fatal_ERROR();	
		USART_Transmit(0x5F);
		return 0;
	}
	
	TIMER_ON();
	uint8_t i,speed;
	int ii;
		
	speed = setGantrySpeed + 31;
	i = 31;
	while(i > 1)
	{
		ii = steps - 200;
		while(steps > ii)
		{
			if (TCNT0 == speed)
			{
				PORTC |= (1<<stepY);
				TCNT0 = 0x00;									//RESET COUNTER
				steps--;
			}
			else if( TCNT0 == speed/2)
			{
				PORTC &= ~(1<<stepY);
			}
				
				
		}//End while steps ii
			
		speed = speed - 1;
		i--;
	}//End while i

	while(steps > 6000){
		if (TCNT0 == setGantrySpeed)
		{
			PORTC |= (1<<stepY);
			TCNT0 = 0x00;									//RESET COUNTER
			steps--;
		}
		else if( TCNT0 == setGantrySpeed/2)
		{
			PORTC &= ~(1<<stepY);
		}
	}


	i = 31;
	ii = 6000;
	speed = setGantrySpeed;
	while(i > 1)
	{
		ii = ii - 200;
		if (ii < 190)
		{
			ii = 0;
			i = 2;
		}
		while(steps > ii)
		{
			if (TCNT0 == speed)
			{
				PORTC |= (1<<stepY);
				TCNT0 = 0x00;									//RESET COUNTER
				steps--;
			}
			else if( TCNT0 == speed/2)
			{
				PORTC &= ~(1<<stepY);
			}
				
				
		}//End while steps ii
		
	
		speed = speed + 1;
		i--;
	}//End while i
		
	TIMER_OFF();
	_delay_us(10);
	PORTC &= ~(1<<stepY);
	
}

/*
* Function Name : move_straightY
 * Description: Moves Gantry Y Axis by "move_Y_units" unit. (1 unit = 1/2 Cell = 25mm)
 * Input Parameters : No. of units/points to move
 * Return value: NONE
 */
void move_diagonal (uint8_t move_diagonal_units)
{	
	step_Diagonal(round_Decimal(move_diagonal_units * steps_per_unitlength));
}


void step_Diagonal (datatype steps)
{

	if (steps > 33000)
	{
		//fatal_ERROR();
	}
		
	TIMER_ON();
			
	uint8_t i,speed;
	int ii;
	
	speed = setGantrySpeed + 31;
	i = 31;
	while(i > 1)
	{
		ii = steps - 200;
		
		
		while(steps > ii)
		{
			if (TCNT0 == speed)
			{
				PORTC |= (1<<stepX)|(1<<stepY);
				TCNT0 = 0x00;									//RESET COUNTER
				steps--;
			}
			else if( TCNT0 == speed/2)
			{
				PORTC &= ~(1<<stepX) &~(1<<stepY);
			}
			
			
		}//End while steps ii
		speed = speed - 1;
		i--;
	}//End while i
	
	

	while(steps > 6000){
		if (TCNT0 == setGantrySpeed)
		{
			PORTC |= (1<<stepX)|(1<<stepY);
			TCNT0 = 0x00;									//RESET COUNTER
			steps--;
		}
		else if( TCNT0 == setGantrySpeed/2)
		{
			PORTC &= ~(1<<stepX) &~(1<<stepY);
		}
	}

	i = 31;
	ii = 6000;
	speed = setGantrySpeed;
	
	while(i > 1)
	{
		ii = ii - 200;
		if (ii < 0)
		{
			ii = 0;
		}
		while(steps > ii)
		{
			if (TCNT0 == speed)
			{
				PORTC |= (1<<stepX)|(1<<stepY);
				TCNT0 = 0x00;									//RESET COUNTER
				steps--;
			}
			else if( TCNT0 == speed/2)
			{
				PORTC &= ~(1<<stepX) &~(1<<stepY);
			}
			
			
		}//End while steps ii
		
		speed = speed + 1;
		i--;
	}//End while i
	
	TIMER_OFF();
	_delay_us(10);
	PORTC &= ~(1<<stepX) &~(1<<stepY);

}

/*
* Function Name : calibrate
 * Description : Initiates the Gantry and Moves to (0,16) for starting point.
 * Input Parameters : NONE
 * Return value: NONE
 */
void calibrate(void)
{	
	//setGantrySpeed = 33;
	//Sends Gantry to TOP RIGHT CORNER
	EM_OFF();
	X_CAL_move_towards_SW();
	Y_CAL_move_towards_SW();
	


	//Sends Gantry to (0,16) 

	dirY_LOW();
	step_straightY(steps_to_Y_equals_16);
	currentYADDR = 16;
	newYADDR = 16;
	
	dirX_HIGH();
	step_straightX(steps_to_X_equals_0);
	currentXADDR = 4;	
	newXADDR = 4;
	
	
	arrived();
	USART_Transmit(0x20|currentXADDR);
	USART_Transmit(0x40|currentYADDR);
	//Send arrived mode with current X and Y address

}

/*
* Function Name : GO
 * Description : Moves the Gantry to specified position.
 *		If EM is OFF : The gantry will move diagonally to the nearest final destination, before moving straight towards the final. Saves time
		If EM is ON  : The gantry will only move straight or in diagonals. Valid Moves are (0,0) to (16,16) OR (16,11) to (10,11). 
					 : If moves invalid, UART will transmit 0xE2. INVALID GO COMMAND
 * Input Parameters : X_addr, Y_addr, Address of final X and Y destination.
 * Return value: NONE
 */

void GO(uint8_t X_addr, uint8_t Y_addr)
{
	//Checks if Addresses are Valid.
	if (X_addr > 25)
	{
		//invalid_GO_command();
		return 0;
	}
	if (Y_addr > 17)
	{
		//invalid_GO_command();
		return 0;
	}
	
	uint8_t difference_X;
	uint8_t difference_Y;
	
	difference_X = 0;
	difference_Y = 0;
	
	
	//Set directions pins and calculate differences
	if (X_addr > currentXADDR)
	{
		dirX_HIGH();
		difference_X = X_addr - currentXADDR;
	}
	else if (X_addr < currentXADDR)
	{
		dirX_LOW();
		difference_X = currentXADDR - X_addr;
	}
	
	if (Y_addr > currentYADDR)
	{
		dirY_HIGH();
		difference_Y = Y_addr - currentYADDR;
	}
	else if (Y_addr < currentYADDR)
	{
		dirY_LOW();
		difference_Y = currentYADDR - Y_addr;
	}
		
		if ( (PIND & (1<<ena_EM)))			//CHECKS IF EM IS ON
		{ 
			if (difference_X == 0)
			{
				overshootMode = 2;
				move_straightY(difference_Y);
				currentYADDR = Y_addr;
				arrived();
				USART_Transmit(0x20|currentXADDR);
				_delay_ms(1);
				USART_Transmit(0x40|currentYADDR);
				_delay_ms(1);
			}
			else if (difference_Y == 0)
			{
				overshootMode = 1;
				move_straightX(difference_X);
				currentXADDR = X_addr;
				arrived();
				USART_Transmit(0x20|currentXADDR);
				_delay_ms(1);
				USART_Transmit(0x40|currentYADDR);
				_delay_ms(1);
			}
			
			else if (difference_X == difference_Y) //diagonal
			{
				overshootMode = 3;
				move_diagonal(difference_X);
				currentYADDR = Y_addr;
				currentXADDR = X_addr;
				arrived();
				USART_Transmit(0x20|currentXADDR);
				_delay_ms(1);
				USART_Transmit(0x40|currentYADDR);
				_delay_ms(1);
			}
			else
			{
				invalid_GO_command(); //EM On and Moves are not straight nor diagonal			
				return 0;
			}
			
		}
		
		else if(!(PIND & (1<<ena_EM)))//EM is OFF In any Direction other than queen.
		{
			if (difference_X > difference_Y)
			{
				move_diagonal(difference_Y);
				move_straightX(difference_X - difference_Y);
				currentYADDR = Y_addr;
				currentXADDR = X_addr;
				arrived();
				USART_Transmit(0x20|currentXADDR);
				_delay_ms(1);
				USART_Transmit(0x40|currentYADDR);
				_delay_ms(1);
			}
			
			else if (difference_X < difference_Y)
			{
				move_diagonal(difference_X);
				move_straightY(difference_Y -  difference_X);
				currentYADDR = Y_addr;
				currentXADDR = X_addr;
				arrived();
				USART_Transmit(0x20|currentXADDR);
				_delay_ms(1);
				USART_Transmit(0x40|currentYADDR);
				_delay_ms(1);
			}
			
			else if (difference_X == difference_Y)
			{
				move_diagonal(difference_X);
				currentYADDR = Y_addr;
				currentXADDR = X_addr;
				arrived();
				USART_Transmit(0x20|currentXADDR);
				_delay_ms(1);
				USART_Transmit(0x40|currentYADDR);
				_delay_ms(1);
			}
			}
			
	//arrived();	
			
}

/*
* Function Name : USART_INIT
 * Description: Enables UART for 20MHz clock BAUD 9600 and Receive INterrupt and 8 bit data
 * Input Parameters : NONE
 * Return value: NONE
 */
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

/*
* Function Name : USART_interrupt_ENA
 * Description: Enables USART Receive interrupt
 * Input Parameters : None
 * Return value: None
 */
void USART_interrupt_ENA(void)
{
	
	UCSR0B |= (1<<RXCIE0);
	sei();
}

/*
* Function Name : USART_interrupt_DIS
 * Description: Disables USART Receive interrupt
 * Input Parameters : None
 * Return value: None
 */
void USART_interrupt_DIS(void)
{
	
	UCSR0B &= ~(1<<RXCIE0);
	//DRD &= ~(1<<DDD0)
	cli();
}

/*
* Function Name : USART_Transmit
 * Description: Transmit the input parameters with UART
 * Input Parameters : 8- BIT Data to be transmitted
 * Return value: NONE
 */
void USART_Transmit(uint8_t data)
{

	//UART_lastSentByte = data;
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

/*
* Function Name : get_MODE
 * Description: Returns the value of 3 MSB from input to get the mode. (See UART Protocol)
 * Input Parameters : UART Data received to be decoded.
 * Return value: 3 MSB from the input. (Values 0-7)
 */
uint8_t get_MODE(uint8_t input){
	
	//Returns the integer of input bit[7:5]
	//Returns a value from 0-7
	return (input >> 5);
}

/*
* Function Name : get_DATA
 * Description: Returns the value of 5 LSB from input to get the data. 
			  : Data will have different meaning depending on MODE (See UART Protocol)
 * Input Parameters : UART Data received to be decoded.
 * Return value: 5 LSB from the input. (Values 0-32)
 */
uint8_t get_DATA(uint8_t input){
	
	//Returns the integer of input bit[4:0]
	//Returns a value from 0-31
	return (input&0x1F);
}

/*
* Function Name : UART_decode_Command
 * Description: Decodes UART command and carry out the command
 * Input Parameters : NONE
 * Return value: NONE
 */
void UART_decode_Command(uint8_t UART_lastRecievedByte){
	
		// Enables Interrupt to send BUSY Error Code if a UART message is received 
		// while busy carrying out command. 
		//USART_interrupt_ENA();			
		
		
		uint8_t mode_recieved,data_recieved;
		mode_recieved = get_MODE(UART_lastRecievedByte);
			
		data_recieved = get_DATA(UART_lastRecievedByte);
			
		switch (mode_recieved)
		{
			case 1:		//XADDR
			newXADDR = data_recieved;
			break;
				
			case 2:		//YADDR
			newYADDR = data_recieved;
			break;
				
			case 3:		//RFID Mode
			if ( data_recieved == 0x1A )		//if scan request
			{
				uint8_t Type_of_Piece;
				Type_of_Piece = RFID_read();
				USART_Transmit(0x60|Type_of_Piece);
			}
			else
			{
				//invalid_UART_command();
			}
				
			break;
				
			case 4:		//EM Control
			
			//0xFF >> ON; 0x0A >> FLIP; Else OFF
			//Although 0x00 is defined as OFF;
				
				if (data_recieved == 31)
				{
				EM_ON();		
				EM_ON_TX();		//Sends back confirmation
				}
				
				else if (data_recieved == 10)
				{
				EM_FLIP(); 
				EM_FLIP_TX();
				}
				
				else
				{
					
					EM_OFF();
					_delay_ms(500);
					EM_ON();
					_delay_ms(750);
					EM_OFF();
					EM_OFF_TX();
					
				}													
				
			break;
				
			case 5:		//GO MODE
			
				GO(newXADDR,newYADDR);		//Go to last sent X,Y position
				
			break;
				
			//CASE 6 Arrived Not Relevant
				
			case 7:		//ELSE MODE
				
			switch(data_recieved){
				case 0:	//Reset Gantry
				calibrate();
				break;
					
				//CASE1 NO RFID
					
				case 6:	//RESEND DATA
				//USART_Transmit(UART_lastSentByte);
				break;
					
				default:
				//invalid_UART_command();
				break;
	
			}
			break; //CASE MODE 7
				
			default:
				//invalid_UART_command();
				//fatal_ERROR();
			break;
				
		} //END SWITCH 
			
	//USART_interrupt_DIS();
	
}

/*
* Function Name : SPI_init
 * Description: Initialize SPI to begin transmission
 * Input Parameters : NONE
 * Return value: NONE
 */
void SPI_init()
{
	//Disable Power Reduction for SPI
	PRR &= ~(1<<PRSPI);
	//Set output of MOSI,SS,SCK and Reset PinB1 for RFID
	//DDRB = (1<<SCK_RF)|(1<<MOSI_RF)|(1<<SS_RF)|(1<<RST_RF);
	//DDRB &= ~(1<<MISO_RF);
	
	// enable SPI, set as master, and clock prescaler to 1/128
	SPCR |= (1 << SPE) | (1 << MSTR) | (1 << SPR1) | (1 << SPR0);

}

/*
* Function Name :SPI_end
 * Description: Terminates SPI connection
 * Input Parameters : NONE
 * Return value: NONE
 */
void SPI_end()
{
	PRR |= (1<<PRSPI);		//Enables Power Reduction for SPI
	SPCR &= ~(1<<SPE);		//Disables SPI
}


/*
* Function Name : Interrupt for UART Receive Command
 * Description : If a command is received while microcontroller is busy, will transmit Gantry Busy Err Code
 * Input Parameters : None
 * Return value: None
 */
ISR(USART_RX_vect)
{
	USART_Receive();		//Clears interrupt flag
	busy_GANTRY();			//Send BUSY COMMAND
}
