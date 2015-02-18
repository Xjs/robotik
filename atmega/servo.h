#ifndef SERVO_H
#define SERVO_H

#include <math.h>

/////////////////////////////////////////////////////////////////////
// Einfache Ansteuerung fuer zwei Servos.
// 2009. Benjamin Reh, Sven Ebser, Joachim Schleicher
//
// Wir verwenden hier den Hardware-Timer, um das Signal zu erzeugen.
//
// Grundlagen zur Servo-Ansteuerung:
// http://www.rn-wissen.de/index.php/Servos
/////////////////////////////////////////////////////////////////////

#define SERVO_MIN 1000  // Links-Anschlag des Servos
#define SERVO_MAX 2000  // Rechts-Anschlag des Servos

// Steering-PWM
#define BASE_S 1500
#define RIGHT (1800-1500) // initial value of 1844 makes servo emit sounds, so it was decreased a little	
#define LEFT (1170-1500)

#define BASE 1500
#define FORWARD (1952-1500)
#define BACK (1000-1500)

void servoInit();
void setServo(uint8_t nr, uint16_t us);

// Steering and driving functions
void steer(float deg);
void drive(float speed);

#endif
