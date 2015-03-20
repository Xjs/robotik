/* 
 *	Basis
 *	2009 Benjamin Reh und Joachim Schleicher
 */

#include <avr/io.h>
#include <stdlib.h> // enthaelt itoa, ltoa
#include "uart.h"

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


//Zeichenkette empfangen (Laenge: 10 Byte)
unsigned char *uart_gets(void) {
	unsigned char *buffer = (unsigned char *) malloc(sizeof(char)*(MESSAGE_SIZE));
	
	if (buffer != NULL) {
		int i;
		for(i = 0; i < MESSAGE_SIZE; i++) {
			unsigned char c;
			
			// get first char in any case, block until one is there
			// after first char, try to read whole message, but don't block
			if (i == 0 || uart_data_waiting()) {
				c = uart_getc();
			}
			if (buffer[i] = c) {
				continue;
			}
			else {
				return buffer;
			}
		}
		//buffer[MESSAGE_SIZE-1] = '\0';
		// Check if message is complete
		if (buffer[MESSAGE_SIZE-1] == 0)
			return buffer; 
		else
			return NULL;
	}
	else {
		return NULL;
	} 	
}
