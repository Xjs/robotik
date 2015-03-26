#!/usr/bin/python

from sympy import *
from math import sin, cos, sqrt, atan2, pi

RADIUS = 0.5 # meters, TODO: measured value
# TODO: make this radius-independent
CCW = -1 #TODO: glevF changed signs for CCW and CW to match steer function - does this affect navigation calculations?
CW = 1
 # TODO: measure what distance between line and GPS position can be deemed
 # a deviation from our path
THRESHOLD = 0.00001

def distance(a, b):
	x1, y1 = a
	x2, y2 = b
	return sqrt((x1-x2)**2 + (y1-y2)**2)

def oriented_angle(v1, v2):
	dot = v1[0]*v2[0] + v1[1]*v2[1]
	det = v1[0]*v2[1] - v1[1]*v2[0]
	return pi + atan2(det, dot)

class Navigator:
	def __init__(self, tracker):
		# Tracker be a mgps.GPSTracker object
		self.tracker = tracker
		self.radius = RADIUS
	
	def setRadius(self, r):
		"""Set curve radius used for internal calculations"""
		# TODO: needs to be converted to lat/lon units
		self.radius = r
		
	def navigate(self, target):
		"""
		Navigate to a target point, based on my current position.
		
		@args target	target point
		@returns	((direction, angle, radius), (start, end))
			first tuple: describes circle arc
				direction (CW or CCW)
				oriented angle (direction * angle)
				radius
			second tuple: describes line to target
				start point of line (tangent to circle)
				end point of line (target)
		"""
		r = self.radius
		t_latitude, t_longitude = target
		target = Point(*target)
		my_latitude, my_longitude = self.tracker.getPosition()
		me = Point(my_latitude, my_longitude)
		orientation = self.tracker.getOrientation()
		# TODO: Does the following always work, did I understand the trig correctly?
		midpoint_a = (my_latitude - r * sin(orientation), my_longitude + r * cos(orientation))
		midpoint_b = (my_latitude + r * sin(orientation), my_longitude - r * cos(orientation))
		distance_a = distance(midpoint_a, target)
		distance_b = distance(midpoint_b, target)
		if distance_a < distance_b:
			direction = CCW
			midpoint = Point(*midpoint_a)
		else:
			direction = CW
			midpoint = Point(*midpoint_b)
		c = Circle(midpoint, r)
		s = Segment(midpoint, target)
		thales_circle = Circle(s.midpoint, s.length/2.0)
		tangent_points = thales_circle.intersection(c)
		vec_l = (tangent_points[0]-midpoint).args
		vec_r = (tangent_points[1]-midpoint).args
		vec_m = (me-midpoint).args
		
		for v, p in [(vec_l, tangent_points[0]), (vec_r, tangent_points[1])]:
			a = oriented_angle(vec_m, v)
			if sign(a) == direction:
				start = p
				angle = a
		
		return ((direction, angle, r), (start, target.args))
	
	def on_track(self, line):
		"""Are we still on track? If not, better re-navigate"""
		if line is None:
			return False
		else:
			return (distance(Line(*line), self.tracker.getPosition()) < TRESHOLD)
		
