#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from controlServos import *

DEFAULT = 0.07	#It was observed that the steering servo's zero-position 
				#(obtained by steerS(0.0)) has a small offset to the right.
				#To set the wheels exactly straight ahead this default value
				#was introduced.

#The functions defined in this file serve the purpose of abstracting from the
#close-to-hardware implementation of the same functionality in conrolServos.py.
#For higher calculations these following functions are used, since they are
#fitted for the usage of values in meters and seconds.

def stop():		#halt the car
	driveS(0)


def drive(speed):	 #drive at speed in m/s
	speedmessage = (speed/1.6)*0.2
	driveS(speedmessage)

	
def steer(radius):
	#This method steers by input of a curve radius in m.
	#The curve radius is approximated by f(x) = 0.715 * 1/deg - based on
	#measurements.
	#radius is the curve radius (min. -0.715 for full right, min. 0.715 for full left) 
	
	if radius == 0.0: 	#steer straight
		steerS(DEFAULT)
		
	if (abs(radius) < 0.715): 	#radius is invalid
		return
	else:
		deg = 0.715/radius
		steerS(deg)
		return

def steer_at(radius, speed): 	#combination of steer() and drive()
	steer(radius)
	drive(speed)
	
if __name__ == "__main__": 		#can be used to initialize the cruise control
	drive(0.0)
