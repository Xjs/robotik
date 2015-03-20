/* 
 *	Basis
 *	2009 Benjamin Reh und Joachim Schleicher
 */

#include <avr/io.h>
#include <stdlib.h> // enthaelt itoa, ltoa
#include <assert.h>
#include <util/delay.h>
#include "uart.h"
#include "servo.h"


//Schnittstelle initialisieren:
// USART-Init
void uartInit()
{
	UCSR0B |= (1 << TXEN0 )|(1 << RXEN0 );	// UART Senden und empfangen einschalten
	UBRR0 = UBRR_VAL;				//Baudrate einstellen, die im Header-File definiert wurde
}

// Ein Zeichen senden
int uart_putc(unsigned char c)
{
	while(!(UCSR0A & (1 << UDRE0))); 	// warte, bis UDR bereit ist, d.h. letztes Zeichen den Sendepuffer verlassen hat
	UDR0 = c;				//Zeichen senden
	return 0;
}

//ganze Zeichenkette senden
void uart_puts (char *s)
{
	while (*s)
	{   				// so lange *s != '\0' also ungleich dem "String-Endezeichen" 
		uart_putc(*s);
		s++;
	}
}

//ganze Zeichenkette aus program space senden
void uart_puts_pgm (const char* PROGMEM  str)
{
	while (1)
	{   				// so lange c != '\0' also ungleich dem "String-Endezeichen" 
		char c = (char) pgm_read_byte (str);
		uart_putc(c);
		if ('\0' == c)
			return;
		str++;
	}
}

//Zahl ausgeben
void uart_puti (int16_t i) 
{
	char buffer[10];
	itoa(i, buffer, 10);
	uart_puts(buffer);
}


//Ein Zeichen empfangen
unsigned char uart_getc(void)
{
	while (!(UCSR0A & (1<<RXC0)));	// warten bis Zeichen verfuegbar
		return UDR0;		// Zeichen aus UDR an Aufrufer zurueckgeben
}

void uart_putm(unsigned char *message)
{
	unsigned short int i;
	for (i = 0; i < STRIPPED_SIZE; i++)
		uart_putc(message[i]);
}

unsigned short int parity(unsigned char byte)
{
	unsigned short int i;
	unsigned short int result = 0;
	for (i = 0; i < 8 * sizeof(unsigned char); i++)
	{
		if (byte & (1 << i))
			result++;
	}
	return result;
}

unsigned short int check(unsigned char *part, unsigned char checksum)
{
	unsigned short int i;
	if (checksum & 0xf0)
		return 0;
	
	for (i = 0; i < PART_SIZE; i++)
	{
		unsigned short int p1, p2;
		p1 = checksum & (1 << (PART_SIZE - i - 1));
		p2 = (parity(part[i]) % 2) == 0;
		if ((p1 && !p2) || (!p1 && p2))
			return 0;
	}
	
	return 1;
}

//Zeichenkette empfangen (Laenge: 10 Byte)
unsigned char *uart_gets(unsigned char *buffer) {
	unsigned short int i, j, count;
	unsigned char c;
	
	count = 0;

	buffer[count++] = '\xff';
	buffer[STRIPPED_SIZE-1] = '\xff';
	/*
	for(i = 0; i < MESSAGE_SIZE; i++)
	{
		buffer[i] = '\xff';
	}
	*/
	
	while (!uart_data_waiting())
		_delay_ms(10);
	
	while (c = uart_getc()) // ignore part of previous message
	{
		if (c == '\xff')
			break;
	}
	
	for (j = 0; j < PARTS; j++)
	{
		for(i = 1; i < PART_SIZE+1; i++) {
			// get first char in any case, block until one is there
			// after first char, try to read whole message, but don't block
			if(!uart_data_waiting())
				return NULL;
			c = uart_getc();
			if (i == PART_SIZE) // checksum byte
			{
				// buffer+(j*(PART_SIZE+1))+1 is the start of the j-th part
				//if (!check(buffer+(j*(PART_SIZE+1))+1, c))
				//{
					// message doesn't match checksum
				//	buffer[0] = 0;
				//}
			}
			else
			{
				//buffer[count++] = c;
			}
		}
	}
	
	uart_puts("hallo");
		
	c = uart_getc();
	buffer[count++] = c;
	
	assert(count == STRIPPED_SIZE);
	
	// count should now be MESSAGE_SIZE
	//buffer[MESSAGE_SIZE-1] = '\0';
	// Check if message is complete
	if (buffer[STRIPPED_SIZE-1] == 0)
		return buffer; 
	else
	{
		buffer[0] = 0;
		return buffer;
	}
}
/*	
	unsigned char *uart_gets(unsigned char *buffer){
	int i;
	unsigned char c;
	
	while (!uart_data_waiting())
		_delay_ms(10);
	
	for(i = 0; i < MESSAGE_SIZE; i++) {		
		// get first char in any case, block until one is there
		// after first char, try to read whole message, but don't block
		c = uart_getc();
		buffer[i] = c;
	}
	
	return buffer;
	
	}
}
*/

