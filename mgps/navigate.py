#!/usr/bin/python

from math import sin, cos, sqrt

RADIUS = 0.5 # meters, TODO: measured value
# TODO: make this radius-independent
LEFT = 0
RIGHT = 1

def distance(a, b):
	x1, y1 = a
	x2, y2 = b
	return sqrt((x1-x2)**2 + (y1-y2)**2)

class Navigator:
	def __init__(self, tracker):
		# Tracker be a mgps.GPSTracker object
		self.tracker = tracker
		
	def navigate(self, target):
		r = RADIUS
		t_latitude, t_longitude = target
		my_latitude, my_longitude = self.tracker.getPosition()
		orientation = self.tracker.getOrientation()
		# TODO: Does the following always work, did I understand the trig correctly?
		midpoint_a = (my_latitude - r * sin(orientation), my_longitude + r * cos(orientation))
		midpoint_b = (my_latitude + r * sin(orientation), my_longitude - r * cos(orientation))
		distance_a = distance(midpoint_a, target)
		distance_b = distance(midpoint_b, target)
		if distance_a < distance_b:
			direction = LEFT
		else
			direction = RIGHT
		# TODO: calculate tangent point
		# TODO: calculate angle from here until tangent
		# TODO: return a circle arc and a straight line which lead to target
