/* 
 *	Basis
 *	2009 Benjamin Reh und Joachim Schleicher
 */
#include <avr/io.h>
#include <inttypes.h>
#include <util/delay.h>
#include <stdlib.h>
#include "uart.h"
#include "adc.h"
#include "pwm.h"
#include "timer.h"
#include "servo.h"

void init();

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

	unsigned char *message = (unsigned char *) malloc(sizeof(char)*(STRIPPED_SIZE));
	if (!message)
		return -1;

	while (1){
//		_delay_ms(6000000);
		
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
}
