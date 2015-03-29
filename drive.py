#!/usr/bin/python

import time
from controlServos import *

def stop():
	driveS(0)

#drives at speed m/s
def drive(speed):
	speedmessage = (speed/1.6)*0.2
	driveS(speedmessage)
	
def drivefor(m):
	speed = 1.3
	s = m/1.3
	drive(1.3)
	time.sleep(s)
	stop()

	
#method that steers by input of curve radius in m and drives at lowest speed
#curve radius is approximated by f(x) = 0.715 * 1/deg
#deg is a float between -1.0 and 1.0 which is used by the atmega's steer method

#rad is the curve radius (min. -0.715 for full right, min. 0.715 for full left) 

def steer_only(radius):
	if (abs(radius) < 0.715):
		return
	else:
		deg = 0.715/radius
		steerS(deg)
		return

def steer(rad):
	if (abs(rad) < 0.715):
		return
	else:
		deg = 0.715/rad
		steerS(deg)
		driveS(0.2)
		return

def steerat(rad, speed):
	if (abs(rad) < 0.715):
		return
	else:
		speedmessage = (speed/1.6)*0.2
		deg = 0.715/rad
		steerS(deg)
		driveS(speedmessage)
		return
	
def stunt():
	steerat(0.5, -0.6)
	time.sleep(0.5)
	steerat(0.0, 0.0)
	
if __name__ == "__main__":
	drive(1.3)
