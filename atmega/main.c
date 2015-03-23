/* 
 *	Basis
 *	2009 Benjamin Reh und Joachim Schleicher
 */
#include <avr/io.h>
#include <avr/interrupt.h>
#include <inttypes.h>
#include <util/delay.h>
#include <stdlib.h>
#include <stddef.h>
#include "uart.h"
#include "adc.h"
#include "pwm.h"
#include "timer.h"
#include "servo.h"

void init();

/* Define two buffers for interrupt-based reading UART data
 * We write into one buffer via interrupts
 * When we want to read out a buffer, we first switch the current buffer
 */

#define BUFFER_SIZE 64

unsigned char buffer[2][BUFFER_SIZE];
unsigned short int buffer_level[2];
unsigned short int ab; // active buffer 0 or 1
unsigned short int buffer_status[2]; // 0: nothing special, 1: start byte received, 2: start and end byte received, 3: buffer full

#define BUFFER_NOTHING 0
#define BUFFER_START 1
#define BUFFER_END 2
#define BUFFER_FULL 3

#define START_OF_MESSAGE '\xff'
#define END_OF_MESSAGE '\0'

void switch_buffers(void)
{
	ab = ab ? 0 : 1;
}

void empty_buffer(unsigned int b)
{
	buffer_level[b] = 0;
	buffer_status[b] = BUFFER_NOTHING;
}

char *find_message(unsigned char *buffer, size_t buffer_size)
{
	int i;
	int found = 0;
	char *result = NULL;
	for (i = 0; i < buffer_size && buffer[i]; i++)
	{
		if (buffer[i] == START_OF_MESSAGE)
		{
			result = buffer+i;
		}
		else if (result && buffer[i] == END_OF_MESSAGE)
		{
			found = 1;
		}
	}
	
	if (found)
		return result;
	else
		return NULL;
}

int main(void)
{
	//Initialisierung ausfuehren
	
	init();
	
	// 1x Ground auf dem MC mit Schaltung verbinden reicht aus. 
	// Test Lenkung ACHTUNG PORTB0 = Servo 0
	//steer(0.5, 2000);
	//steer(-0.5, 2000);
	//steer(0, 2000);
	//setServo(0, LEFT);
	//_delay_ms(3000);
	//setServo(0, BASE_S);
	//_delay_ms(3000);
	//setServo(0, RIGHT);
	//_delay_ms(3000);	
	//setServo(0, BASE_S);
	//_delay_ms(3000);		
	
	// Test Motor ACHTUNG PORTB1 = Servo 1
	//drive(0.5, 2000);
	//drive(0, 2000);
	//drive(-0.5, 2000);
	//_delay_ms(60000);
	//setServo(1, (BASE + (0.9)*FORWARD));
	//_delay_ms(2000);

	unsigned int rb; // read buffer
	unsigned char *message;
//	unsigned char *message = (unsigned char *) malloc(sizeof(char)*(STRIPPED_SIZE));
//	if (!message)
//		return -1;

	while (1)
	{
		while (buffer_status[ab] < BUFFER_END)
		{
			// no message received -- do nothing
			;
		}
		
		rb = ab;
		// message received
		switch_buffers();
		
		message = find_message(buffer[rb], BUFFER_SIZE);
		if (message) {
			// handeln Sie!
			uart_puts(":");
			uart_puts(message);
			uart_puts(";");
		}
		empty_buffer(rb);
//		_delay_ms(6000000);
/*		
		uart_gets(message);
		
		if(0 && message[0] == (unsigned char)'\xff' && message[STRIPPED_SIZE-1] == (unsigned char) '\x00') {
			uart_puts("=");
			uart_putm(message);
			uart_puts("=");

			unsigned char m_deg[sizeof(float)];
			unsigned char m_speed[sizeof(float)];
			
			unsigned short int i;
			for (i=0; i < sizeof(float); i++) {
				m_deg[i] = message[i+1];
				m_speed[i] = message[i+sizeof(float)+1];
			}
			float deg;
			float speed;
			deg = (float) *((float*)m_deg);
			deg -= 0.07; //Gauge to straight ahead.
			speed = (float) *((float*)m_speed);
			
			//Dummy
		//	float deg = 0.5;
		//	deg -= 0.07;
		//	speed = 0.15;
			//Dummy END
			
			steer(deg);
			drive(speed);
		}	
		else
		{
			_delay_ms(1);
			uart_puts(":");
			uart_putm(message);
			uart_puts(":@");
		}
*/
	}

	free(message);
}


//INIT
void init()
{
	uartInit();   // serielle Ausgabe an PC
	ADCInit(0);   // Analoge Werte einlesen
	PWMInit();    // Pulsweite auf D6 ausgeben 
	timerInit();  // "Systemzeit" initialisieren
	servoInit();  // Servoansteuerung initialisieren
	sei(); // // Enable the Global Interrupt Enable flag so that interrupts can be processed
}

ISR(USART_RXC_vect)
{
	char received_byte;
	received_byte = UDR0;
	if (buffer_level[ab] < BUFFER_SIZE)
	{
		buffer[ab][buffer_level[ab]++] = received_byte;
		if ((buffer_status[ab] == BUFFER_NOTHING && received_byte == START_OF_MESSAGE) || 
			(buffer_status[ab] == BUFFER_START && received_byte == END_OF_MESSAGE))
		{
			buffer_status[ab]++;
		}
	}
	else
	{
		buffer_status[ab] = BUFFER_FULL;
	}
}
