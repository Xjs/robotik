#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

MAX_DIST = 1.5
SPEED_OF_SOUND = 343.
PULSE_WIDTH = 0.00001

GPIO.setmode(GPIO.BCM)

#Ultrasonic sensors: [LEFT, RIGHT]
trig = [18, 27]
echo = [24, 23]

for t, e in zip(trig, echo):
	GPIO.setup(t, GPIO.OUT)
	GPIO.setup(e, GPIO.IN)

def distance(sensor):

	#This function receives an int for identifying the ultrasonic sensors:
	#0 equals the sensor on the left of the robot, 1 equals the sensor on the
	#right.
	#The respective sensor sends an ultrasonic signal and receives its echo.
	#From the elapsed time between sending the signal and receiving the echo,
	#this function calculates the distance to the closest object in the range
	#of the sensor.

	time.sleep(0.01) 				 #give the sensor some time to relax
	GPIO.output(trig[sensor], True)	 #start signal transmission
	time.sleep(PULSE_WIDTH)			 #keep it up for 0.01 ms
	GPIO.output(trig[sensor], False) #stop signal transmission
	
	startTime = time.time()
	stopTime = time.time()
	st = startTime
	
	#write startTime
	while GPIO.input(echo[sensor]) == 0 and startTime-st < 2.*MAX_DIST/SPEED_OF_SOUND:
		startTime = time.time()
	
	#write time of signal reaching sensor
	while GPIO.input(echo[sensor]) == 1 and stopTime-startTime < 2.*MAX_DIST/SPEED_OF_SOUND:
		stopTime = time.time()
	
	timeElapsed = stopTime - startTime
	
	#The distance equals the elapsed time times sonic speed divided by two
	#because the distance is traveled twice.
	distance = (timeElapsed * SPEED_OF_SOUND) / 2
	if distance > MAX_DIST or stopTime < startTime:
		return -1.0
	else:
		return distance

if __name__ == "__main__":
	start = time.time()
	for i in xrange(2):
		distance(0)
		distance(1)
	end = time.time()
	print end-start

