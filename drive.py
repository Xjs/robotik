#!/usr/bin/python

import time
from sendMessage import *

#speed = 1.6


#drives for m meters at speed of 1.6 m/s

#def drive(m):
#	s = m/speed
#	sendMessage(0.0, 0.2) #start driving
#	time.sleep(s)		  #drive m meters
#	sendMessage(0.0, 0.0) #stop car
def stop():
	sendMessage(0.0, 0.0)

def drive():
	sendMessage(0.5, 0.2)

def driveat(speed):
	speedmessage = (speed/1.6)*0.2
	sendMessage(0.0, speedmessage)

	
#method that steers by input of curve radius in m and drives at lowest speed
#curve radius is approximated by f(x) = 0.715 * 1/deg
#deg is a float between -1.0 and 1.0 which is used by the atmega's steer method

#rad is the curve radius (min. 0.715 for full right, min. -0.715 for full left) 
 
def steer(rad):
	if (abs(rad) < 0.715):
		return
	else:
		deg = 0.715/rad
		sendMessage(deg, 0.2)
		return
def steerat(speed,rad):
	if (abs(rad) < 0.715):
		return
	else:
		speedmessage = (speed/1.6)*0.2
		deg = 0.715/rad
		sendMessage(deg, speedmessage)
		return
	
def stunt:
	sendMessage(-0.6, 0.5)
	time.sleep(0.5)
	sendMessage(0.0, 0.0)
	
if __name__ == "__main__":
	drive()
