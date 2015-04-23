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
#TODO: this SPEED was the value for low battery - what did we use for a full battery?
SPEED = 1.5 #for low battery: SPEED needs to be increased in order to drive 
			#with the usual speed and guarantee correct course calculations
#SPEED = ??? #for full battery
STDEV = 5 #deviation of GPS data in meters
line = None

def angular_speed(radius, speed):
	return speed/(2*pi*radius)

def is_at(current, target):
	#Returns the approximated distance between the current Position and the target.
	if current is None or target is None:
		return False
	else:
		dis = great_circle_distance(current, target)
		print("approximated Distance = ", dis)
		return dis < STDEV
	
def correct_course(direction, angle, radius, speed=SPEED, watcher=None):
	#Calculates the path to be driven to correct the course and also executes
	#the correction.
	CAL = 1.2	#TODO: What exactly does CAL stand for? And how was the value obtained?
	print "this is correct_course!"
	print "direction = ", direction
	print "angle = ", angle
	print "radius = ", radius
	#Calculate circular path to be driven.
	time_for_circle = 1/angular_speed(0.64, 1.1) #Values given to angular_speed 
												 #are finetuned by measuring.
	amount_of_circle = angle/(2*pi)
	time_needed = abs(amount_of_circle * time_for_circle) #abs is important so 
														  #the robot doesn't circle 
														  #infinitely because it 
														  #thinks it needs a 
														  #negative amount of time.
	print "time_for_circle = ", time_for_circle
	print "amount_of_circle = ", amount_of_circle
	print "time_needed = ", time_needed

	start = time.time()
	steer_at(direction*radius, 1.6)
	while ((time.time() - start) < time_needed+CAL):
		try:
			#watcher.obstancle()	-	Commented out because it sometimes causes 
										#the robot to dodge obstacles not actually 
										#present, leading to many unnecessary
										#course corrections.
			pass
		except AttributeError:
			pass
	stop()
	steer_at(0, speed)		#Drive straight after course was corrected.

def mainRoutine(target):
	if target is None or len(target) != 2:	#Check if input is correct.
		print "no reasonable target given"
		return
		
	#Initialize needed objects.
	#Offset values were obtained by calibration of the compass.
	tracker = GPSTracker(n_averages = 3, x_offset = -112.0, y_offset = 51.0, angle_offset = 2*pi-83.088772881)
	navigator = Navigator(tracker)
	navigator.setRadius(RADIUS)
	
	watcher = Watcher()
	
	speed = SPEED

	steer(0) #Make sure car steers ahead before beginning its journey.
	
	watcher.obstancle() #Check for obstacles.
	
	#Obtain GPS coordinates - if not accessible, wait for fix.
	curPos = None
	while curPos is None:
		print "no fix yet, sleeping a bit"
		time.sleep(1)
		curPos = tracker.getPosition()
	print curPos
	
	line = None
	circle = None
	
	while True:
		if is_at(curPos, tracker.getPosition()): 	#Car stands still
			print "standing"
			start = time.time()
			print "driving at", speed
			drive(speed)					 #Drive for a few meters.
			while (time.time() - start) < 2: #While driving save positions to tracker.
				watcher.obstancle()
				tracker.getPosition()
			stop()
		
			line = None
		else:
			driving = True
		
		
		if is_at(tracker.getPosition(), target):
			print "target reached"
			stop()
			break
		
		#Check if car is still on track - if not, renavigate.
		if not navigator.on_track(line):
			#Going through the while-true-loop for the first time also reaches
			#this code because line was not yet set.
			print "not on track"
			stop() 	#Necessary for correct course to work properly. 
			circle, line = navigator.navigate(target)	#Calculate direction to
														#be taken to reach
														#target.
			print "circle = ", circle
			print "line = ", line
			correct_course(*circle, speed=speed, watcher=watcher)
			drive(speed)
			driving = True
		
		if driving:
		#Car is still driving - save position and check for obstacles. 
			print "driving"
			curPos = tracker.getPosition()
			watcher.obstancle()
	
if __name__ == '__main__':
	try:
		target = tuple(float(i) for i in sys.argv[1:3]) #Check if input is
														#correct (i.e. if 
														#numbers are given as
														#command line arguments).
	except ValueError:									#If not, set target to
														#None and let the
														#mainRoutine() handle it.
		target = None
	mainRoutine(target)
