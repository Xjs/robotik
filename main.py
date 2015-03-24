#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from mgps import *
import time
import sys
from math import sin, cos, acos, pi
from obstancle import *
from drive import *
from mgps/navigate import *

angularSpeed = 1.6 * (2*pi) #per second

tracker = GPSTracker()
navi = Navigator(tracker)
navi.setRadius(0.715)
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

def approxDistance(target):
	a = tracker.getPosition()
	b = target
	
	pk = 180/3.14169
	
	a_lat = a[0] / pk
	a_long = a[1] / pk
	
	b_lat = b[0] / pk
	b_long = b[1] / pk
	
	t1 = cos(a_lat)*cos(a_long)*cos(b_lat)*cos(b_long)
	t2 = cos(a_lat)*sin(a_long)*cos(b_lat)*sin(b_long)
	t3 = sin(a_lat)*sin(b_lat)
	
	tt = acos(t1 + t2 + t3)
	
	return 6366000*tt
	
def correctCourse():
	(direction, angle, rad),(start,target) = navigate(target)
	s = angle/angularSpeed
	
	start = time.time()
	steer(0.715)
	while ((time.time() - start) < s):
		pass
	steer(-0.07)

def mainRoutine(target):
	#Hindernis checken
	obstancle()
	# GPS-Position bekommen
	curPos = tracker.getPosition()
	time.sleep(2)
	while True:
		if curPos == tracker.getPosition():	#car stands still
			# Entweder: (Re-)Initialisierung – geradeausfahren, Orientierung holen (Kompass koennen wir glaub ich nicht vertrauen), kreiseln, bis man drauf zuschaut, 			  anfangen, geradeaus zu fahren
			start = time.time()
			drive(1.6)			#drive for 5m
			while (time.time() - start) < 3:	#while driving (ca. 3 s) save positions to tracker
				stop()
				tracker.getPosition()
#			orientation = tracker.getOrientation()
			#check if orientation is correct
			(direction, angle, rad),(start,target) = navigate(target)
			if on_track((start,target)) == True:
				#if so: drive for approximate number of meters until destination
				drive(1.6)
				if tracker.getPosition == target: #target reached, stop car
					stop()
					break
			else:
				correctCourse()
				
		else: #car is moving
		# Oder: Wir fahren noch
		# 	immer mal wieder Position updaten
			tracker.getPosition()
		# 	mit der Linie vergleichen, und wenn wir zu sehr abweichen, mal wieder von vorn
#			orientation = tracker.getOrientation()
			(direction, angle, rad),(start,target) = navigate(target)
			if on_track((start,target)) == True:
				drive(1.6) 
				if tracker.getPosition == target: #target reached, stop car
					stop()
			else:
				correctCourse()
				
		
	
# Ausweich-Subroutine: Lenk solange vom Hindernis weg, bis es nicht mehr da ist
# Wenn es nicht weggeht oder auf beiden Seiten eines gemessen wird… vielleicht rückwärts fahren?

if __name__ == '__main__':
	target = sys.argv
	mainRoutine(target)
