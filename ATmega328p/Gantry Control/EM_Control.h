/*
* Function Name :EM_ON
 * Description: Turns on Electromagnet
 * Input Parameters : NONE
 * Return value: NONE
 */
void EM_ON (void)
{
	PORTD |= (1<<PORTD5)|(1<<PORTD6) ;
	PORTD &= ~(1<<PORTD7);
	_delay_ms(5);

	
}

/*
* Function Name :EM_OFF
 * Description: Turns off Electromagnet
 * Input Parameters : NONE
 * Return value: NONE
 */
void EM_OFF (void)
{
	PORTD &= ~(1<<PORTD5) &~(1<<PORTD6) &~(1<<PORTD7);
	_delay_ms(5);

}

/*
* Function Name :EM_FLIP
 * Description: Flips Electromagnet Polarity to Topple King at Checkmate
 * Input Parameters : NONE
 * Return value: NONE
 */
void EM_FLIP (void)
{
	EM_ON();
	_delay_ms(500);
	
	PORTD &= ~(1<<PORTD6);
	PORTD |=  (1<<PORTD7);
	
	_delay_ms(1250);
	EM_OFF();
	
	
	
}