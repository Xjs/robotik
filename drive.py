#!/usr/bin/python

import time
from sendMessage import *

speed = 1.6


#drives for m meters at speed of 1.6 m/s

#def drive(m):
#	s = m/speed
#	sendMessage(0.0, 0.2) #start driving
#	time.sleep(s)		  #drive m meters
#	sendMessage(0.0, 0.0) #stop car

def drive():
	sendMessage(0.0, 0.2)

if __name__ == "__main__":
	drive()
