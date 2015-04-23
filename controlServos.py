#!/usr/bin/python
# -*- coding: utf-8 -*-

from RPIO import PWM
import time

servo1 = PWM.Servo()
servo2 = PWM.Servo()

BASE = 1500
RIGHT = (1800-BASE) 
LEFT = (1170-BASE)

FORWARD = (1952-BASE)
BACK = (1000-BASE)


def steerS(deg):
	#Sets steering degree from -1 == hard right to 1 == hard left.
	#The value val for the PWM signal is floored to a multiple of 10 in order to
	#appease RPIO.PWM.
	
	if(deg < -1 or deg > 1):	#deg is invalid
		return
	
	elif (deg < 0):		#steer right
		val = int(BASE + (-deg)*RIGHT)
		val -= (val%10)
		servo1.set_servo(17, val)
		time.sleep(0.5)
		
	elif (deg > 0):		#steer left
		val = int(BASE + deg*LEFT)
		val -= (val%10)
		servo1.set_servo(17, val)
		time.sleep(0.5)
		
	elif (deg == 0):	#steer straight
		servo1.set_servo(17, BASE)
		time.sleep(0.5)
		
def driveS(speed):
	#Sets engine to drive at a speed between -1 == full throttle backwards and 
	#1 == full throttle forwards.
	#The value val for the PWM signal is floored to a multiple of 10 in order to
	#appease RPIO.PWM.
	#Caution: Minimum positive value for speed is 0.2.
	#		  Maximum negative value for speed is about -0.15.
	#		  For speed values : -0.15 < speed < 0.2 the car does not respond.
	
	if(speed < -1 or speed > 1):	#speed is invalid
		return
		
	elif (speed < 0):		#drive backwards
		val = int(BASE + (-speed)*BACK)
		val -= (val%10)
		servo2.set_servo(22, val)	
	
	elif (speed > 0):		#drive forwards
		val = int(BASE + speed*FORWARD)
		val -= (val%10)
		servo2.set_servo(22, val)
	
	elif (speed == 0):		#halt
		servo2.set_servo(22, BASE)

def test():
	#Test function to test basic servo responses using RPIO.PWM.

	# Set servo on GPIO17 (BCM) to (1.6ms)
	servo1.set_servo(17, 1600)
	
	time.sleep(2)

	# Set servo on GPIO17 (BCM) (1.2ms)
	servo1.set_servo(17, 1200)

	time.sleep(2)

	# Clear servo on GPIO17
	servo1.stop_servo(17)
	
	# Set servo on GPIO22 (BCM) to (1.6ms)
	servo2.set_servo(22, 1600)

	time.sleep(2)

	# Set servo on GPIO22 (BCM) (1.2ms)
	servo.set_servo(17, 1200)

	# Clear servo on GPIO22
	servo2.stop_servo(22)
	
def test2():
	#Test function to test implemented functions steerS() and driveS()

	steerS(0.5)
	steerS(-0.5)
	steerS(0)
	driveS(0.3)
	driveS(0)
	driveS(-0.3)

if __name__ == '__main__':
	#test()
	#test2()
