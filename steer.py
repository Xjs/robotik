#!/usr/bin/python

#method that steers by input of curve radius in m and drives at lowest speed
#curve radius is approximated by f(x) = 0.715 * 1/deg
#deg is a float between -1.0 and 1.0 which is used by the atmega's steer method
 
import sendMessage.py
 
def steer(rad):
	deg = 0.715/rad
	sendMessage(deg, 0.2)
