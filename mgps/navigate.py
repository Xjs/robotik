#!/usr/bin/python

from sympy import *
from math import sin, cos, sqrt, atan2, pi

RADIUS = 0.5 # meters (this is a dummy value)

# I changed these values back, otherwise I'd have to filter atan2 data in a complicated way. Better change steer.
CCW = 1
CW = -1

 # TODO: measure what distance between line and GPS position can be deemed
 # a deviation from our path
THRESHOLD = 0.00001

EARTH_RADIUS = 6371000 # metres

def distance(a, b):
	x1, y1 = a
	x2, y2 = b
	return sqrt((x1-x2)**2 + (y1-y2)**2)

def to_rad(arg):
	return 2*pi/360.0 * arg

def to_deg(rad):
    return rad/(2*pi)*360

def point_to_rad(*args):
	for arg in args:
		yield to_rad(arg)

def great_circle_distance(p1, p2):
	# sources: http://www.movable-type.co.uk/scripts/latlong.html
	phi1, lambda1 = point_to_rad(*p1)
	phi2, lambda2 = point_to_rad(*p2)
	delta_phi = abs(phi2-phi1)
	delta_lambda = abs(lambda2-lambda1)
	
	# Equirectangular approximation
	return EARTH_RADIUS*sqrt((delta_lambda * cos((phi1+phi2)/2.0))**2 + delta_phi**2)
	
	# alternatively: Haversine formula
	a = sin(delta_phi/2.0)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda/2.0)**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	return EARTH_RADIUS*c

def distance_to_angular_distance(d):
	return d/EARTH_RADIUS

def angular_distance_to_distance(d):
	return d * EARTH_RADIUS

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
		# convert to angular distance
		self.radius = r
		
	def navigate(self, target):
		"""
		Navigate to a target point, based on my current position.
		
		@args target	target point
		@returns	((direction, angle, radius), (start, end))
			first tuple: describes circle arc
				direction (CW or CCW)
				oriented angle (direction * angle)
				radius in metres
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
		d_lat = to_deg(r*sin(orientation)/EARTH_RADIUS)
		d_lon = to_deg(r*cos(orientation)/EARTH_RADIUS)/(cos(to_rad(my_latitude)))
		midpoint_a = (my_latitude - d_lat, my_longitude + d_lon)
		midpoint_b = (my_latitude + d_lat, my_longitude - d_lon)
		distance_a = distance(midpoint_a, target)
		distance_b = distance(midpoint_b, target)
		if distance_a < distance_b:
			direction = CCW
			midpoint = Point(*midpoint_a)
		else:
			direction = CW
			midpoint = Point(*midpoint_b)
		c = Circle(midpoint, sqrt(d_lat**2+d_lon**2))
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
