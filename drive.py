#!/usr/bin/python

import time
from controlServos import *

DEFAULT = -0.07

def stop():
	driveS(0)

#drives at speed m/s
def drive(speed):
	speedmessage = (speed/1.6)*0.2
	driveS(speedmessage)

#is never actually used, I think	
#def drivefor(m):
#	speed = 1.3
#	s = m/1.3
#	drive(1.3)
#	time.sleep(s)
#	stop()

	
#method that steers by input of curve radius in m and drives at lowest speed
#curve radius is approximated by f(x) = 0.715 * 1/deg
#deg is a float between -1.0 and 1.0 which is used by the atmega's steer method

#rad is the curve radius (min. -0.715 for full right, min. 0.715 for full left) 

def steer(radius):
	if radius == 0.0:
		steerS(DEFAULT)
	if (abs(radius) < 0.715):
		return
	else:
		deg = 0.715/radius
		steerS(deg)
		return

#def steer(radius):
#	steer_only(radius)
#	drive(1.3) #Should be erased: Since i used steer a lot and it should be independent from speed anyway. Also the minimum speed changes apparently so a fixed speed in steering isnt helpful.
#agreed - this function is redundant if it is not used anywhere else - hence why I only uncommented it for now
#I'll check the code for usage of steer()

def steer_at(radius, speed):
	steer(radius)
	drive(speed)
	
def stunt():
	steerat(0.5, -0.6)
	time.sleep(0.5)
	steerat(0.0, 0.0)
	
if __name__ == "__main__":
	drive(1.3)
