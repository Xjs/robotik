#!/usr/bin/python
# -*- coding: utf-8 -*-

from mgps import *
import time
import sys
from math import sin, cos, acos, pi
from obstancle import *
from drive import *
from mgps import GPSTracker
from mgps.navigate import Navigator, THRESHOLD

RADIUS = 0.715
SPEED = 1.5
DEFAULT = -0.07

def angular_speed(radius):
	# TODO: this isn't radius-dependent yet
	# TODO: measure
	# something like
	return (1/radius) * (2*pi) #per second

#----------------
#A simple function that takes two GPS coordinates as input and outputs the distance between them in meter. More approaches can be found here

#private double gps2m(float lat_a, float lng_a, float lat_b, float lng_b) {
#float pk = (float) (180/3.14169);

#float a1 = lat_a / pk;
#float a2 = lng_a / pk;
#float b1 = lat_b / pk;
#float b2 = lng_b / pk;

#float t1 = FloatMath.cos(a1)*FloatMath.cos(a2)*FloatMath.cos(b1)*FloatMath.cos(b2);
#float t2 = FloatMath.cos(a1)*FloatMath.sin(a2)*FloatMath.cos(b1)*FloatMath.sin(b2);
#float t3 = FloatMath.sin(a1)*FloatMath.sin(b1);
#double tt = Math.acos(t1 + t2 + t3);

#return 6366000*tt;
#}
#--------------------

def approxDistance(current, target):
	a = current
	b = target
	
	pk = 180/pi
	
	a_lat = a[0] / pk
	a_long = a[1] / pk
	
	b_lat = b[0] / pk
	b_long = b[1] / pk
	
	t1 = cos(a_lat)*cos(a_long)*cos(b_lat)*cos(b_long)
	t2 = cos(a_lat)*sin(a_long)*cos(b_lat)*sin(b_long)
	t3 = sin(a_lat)*sin(b_lat)
	
	tt = acos(t1 + t2 + t3)
	
	return 6366000*tt
	
def is_at(current, target):
	if current is None or target is None:
		return False
	else:
		return approxDistance(current, target) < THRESHOLD #TODO: THRESHOLD deklarieren
	
def correct_course(direction, angle, radius, watcher = None):
	s = angle/angular_speed(radius)
	
	start = time.time()
	steer(direction*radius)
	while ((time.time() - start) < s):
		try:
			watcher.obstancle()
		except AttributeError:
			pass
	steer(DEFAULT)

def mainRoutine(target):
	watcher = Watcher()
	start=time.time()
	drive(2)
	while(True):
		watcher.obstancle()
		if(start-time.time()>4):
			stop()
	
# Ausweich-Subroutine: Lenk solange vom Hindernis weg, bis es nicht mehr da ist
# Wenn es nicht weggeht oder auf beiden Seiten eines gemessen wird… vielleicht rückwärts fahren?
if __name__ == '__main__':
	try:
		target = tuple(float(i) for i in sys.argv[1:3])
	except ValueError:
		target = None
	mainRoutine(target)
