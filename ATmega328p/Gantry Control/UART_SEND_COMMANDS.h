/*
* Function Name : arrived
 * Description: Transmits UART command for Arrived
 * Input Parameters : NONE
 * Return value: NONE
 */
void arrived(void) 
{
	USART_Transmit(0xDF);
	_delay_ms(1);
}

/*
* Function Name : busy_Gantry
 * Description: Transmits UART command for Gantry BUSY. Not Accepting any Command
 * Input Parameters : NONE
 * Return value: NONE
 */
void busy_GANTRY(void)
{
	//USART_Transmit(0xE5);
}

/*
* Function Name : invalid_GO_command
 * Description: Transmits UART command invalid Move. When EM is ON and 
 *				moves are not directly straight or diagonal.
 * Input Parameters : NONE
 * Return value: NONE
 */
void invalid_GO_command(void)
{
	//USART_Transmit(0xE2);
}

/*
* Function Name : invalid_UART_command
 * Description: Transmits UART command invalid UART Command
 * Input Parameters : NONE
 * Return value: NONE
 */
void invalid_UART_command(void)
{
	//USART_Transmit(0xE3);
}

/*
* Function Name : invalid_UART_command
 * Description: Transmits UART command invalid UART Command
 * Input Parameters : NONE
 * Return value: NONE
 */
void fatal_ERROR(void)
{
	USART_Transmit(0xFF);
}

/*
* Function Name : EM_ON_TX
 * Description: Transmit UART command EM ON. to confirm EM is ON back to the raspberry pi
 * Input Parameters : NONE
 * Return value: NONE
 */
void EM_ON_TX(void)
{
	USART_Transmit(0x9F);
}

/*
* Function Name : EM_OFF_TX
 * Description: Transmit UART command EM OFF. to confirm EM is ON back to the raspberry pi
 * Input Parameters : NONE
 * Return value: NONE
 */
void EM_OFF_TX(void)
{
	USART_Transmit(0x80);
}

/*
* Function Name : EM_OFF_TX
 * Description: Transmit UART command EM FLIP. EM flipping is DONE
 * Input Parameters : NONE
 * Return value: NONE
 */
void EM_FLIP_TX(void)
{
	USART_Transmit(0x8A);
}