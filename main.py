#!/usr/bin/python
# -*- coding: utf-8 -*-

from mgps import *
import time
import sys
from math import sin, cos, acos, pi
from obstancle import *
from drive import *
from mgps import GPSTracker
from mgps.navigate import Navigator
from mgps.helpers import great_circle_distance

RADIUS = 0.715
#SPEED = 0.2 #Testing nessesairy for determening minimum speed. seems to change a lot. Last time it was 3
SPEED = 1.6 # my (Jannis') experience: Everything works fine if you make absolutely sure that you send driveS(0) and nothing else at the time the drive controller is turned on. Sometimes a residual signal is still being sent from last time the program ran, in which case the drive controller thinks this is the zero position. If you make sure that you aren't sending anything greater or less than 0, all speeds are as measured.
STDEV = 10 # meters, deviation of GPS data
line = None

def angular_speed(radius, speed):
	return (2*pi*radius)/speed

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
		dis = great_circle_distance(current, target)
		#dis = approxDistance(current, target)
		print("approximated Distance = ", dis)
		return dis < STDEV
	
def correct_course(direction, angle, radius, speed=SPEED, watcher=None):
	print "this is correct_course!"
	print "direction = ", direction
	print "angle = ", angle
	print "radius = ", radius
	time_for_circle = 1/angular_speed(radius, speed)
	amount_of_circle = angle/(2*pi)
	time_needed = abs(amount_of_circle * time_for_circle) # abs is important so the robot doesn't circle infinitely because it thinks it needs a negative amount of time
	print "time_for_circle = ", time_for_circle
	print "amount_of_circle = ", amount_of_circle
	print "time_needed = ", time_needed
	
	start = time.time()
	steer_at(direction*radius, speed)
	while ((time.time() - start) < time_needed):
		try:
			watcher.obstancle()
		except AttributeError:
			pass
	steer_at(0, speed)

def mainRoutine(target):
	if target is None or len(target) != 2:
		print "no reasonable target given"
		return
		
	tracker = GPSTracker()
	navigator = Navigator(tracker)
	navigator.setRadius(RADIUS)
	
	watcher = Watcher()
	
	speed = SPEED # nicht ueberfluessig?! Vielleicht soll das Programm spaeter mal mit variabler Geschwindigkeit fahren koennen...
	
	#Hindernis checken
	#watcher.obstancle()
	# GPS-Position bekommen
	curPos = None
	while curPos is None:
		# no fix yet
		print "no fix yet, sleeping a bit"
		time.sleep(1)
		curPos = tracker.getPosition()
	print curPos
	
	line = None
	circle = None
	
	while True:
		if is_at(curPos, tracker.getPosition()):	# car stands still
			print "standing"
			# Entweder: (Re-)Initialisierung – geradeausfahren, Orientierung holen (Kompass koennen wir glaub ich nicht vertrauen)
			start = time.time()
			print "driving at", speed
			drive(speed)			#drive for 5m
			while (time.time() - start) < 3:	#while driving (ca. 3 s) save positions to tracker
				watcher.obstancle()
				tracker.getPosition()
			stop()
			# renavigate
			line = None
		else:
			driving = True
		
		# target reached
		if is_at(tracker.getPosition(), target):
			print "target reached"
			stop()
			# stunt()
			break
		
		# 	mit der Linie vergleichen, und wenn wir zu sehr abweichen, mal wieder von vorn
		if not navigator.on_track(line):
			# wenn line noch nicht gesetzt ist (1. Mal), landen wir auch hier
			# jetzt: kreiseln, bis man drauf zuschaut, anfangen, geradeaus zu fahren
			print "not on track"
			stop() # wuerde ich weglassen # ist aber noetig, sonst funktioniert correct_course ja nicht.
			circle, line = navigator.navigate(target)
			print "circle = ", circle
			print "line = ", line
			correct_course(*circle, speed=speed, watcher=watcher)
			#correct_course(circle[0], circle[1], circle[2], speed, watcher)
			drive(speed)
			driving = True
		
		if driving:
		# Wir fahren noch, muessten eigentlich auf unserer Linie sein.
		# 	immer mal wieder Position updaten
			print "driving"
			curPos = tracker.getPosition()
			watcher.obstancle()
	
# Ausweich-Subroutine: Lenk solange vom Hindernis weg, bis es nicht mehr da ist
# Wenn es nicht weggeht oder auf beiden Seiten eines gemessen wird… vielleicht rückwärts fahren?
if __name__ == '__main__':
	try:
		target = tuple(float(i) for i in sys.argv[1:3])
	except ValueError:
		target = None
	mainRoutine(target)
