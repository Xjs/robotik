#!/usr/bin/python

from __future__ import division
from math import sqrt, sin, cos, atan, atan2, pi

DEBUG = True

EARTH_RADIUS = 6371000 # metres

def sign(x):
	"""Return the sign of a number"""
	return cmp(x, 0)

def angle_to_north(start, end):
	"""start, end: geo coordinates.
	Returns the clockwise angle of the given line to north (i. e. the y axis"""
	start_x, start_y = start
	end_x, end_y = end
	
	try:
		angle = pi/2 - atan((end_y-start_y)/(end_x-start_x))
	except ZeroDivisionError:
		angle = pi/2 - (pi/2 * sign(end_y-start_y))
	
	if start_x <= end_x:
		return angle
	else:
		return pi + angle

def normalize(angle):
	"""Normalize a number so that it is an angle in radian between 0 and 2pi"""
	return angle%(2*pi)

def distance(a, b):
	"""Return the cartesian distance between two points"""
	x1, y1 = a
	x2, y2 = b
	return sqrt((x1-x2)**2 + (y1-y2)**2)

def to_rad(arg):
	"""Convert an angle from degrees to radian"""
	return 2*pi/360 * arg

def to_deg(rad):
	"""Convert an angle from radian to degrees"""
    return rad/(2*pi)*360

def point_to_rad(*args):
	"""Convert several angles to radians"""
	for arg in args:
		yield to_rad(arg)

def great_circle_distance(p1, p2):
	"""
	Calculate the distance on the earth between two geo coordinates,
	using the equirectangular approximation (valid for distances up to
	several 10 kilometres)
	"""
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
	"""Convert a distance in metres to a section of a great circle on the
	earth"""
	return d/EARTH_RADIUS

def angular_distance_to_distance(d):
	"""Convert a section of a great circle on the earth to a distance in 
	metres"""
	return d * EARTH_RADIUS

def oriented_angle(v1, v2):
	"""Return the oriented angle between two vectors, that is the angle starting
	at v1 and ending at v2, with a sign indicating the direction (1 is CCW, -1
	is CW)"""
	dot = v1[0]*v2[0] + v1[1]*v2[1]
	det = v1[0]*v2[1] - v1[1]*v2[0]
	return atan2(det, dot)

def debug_print(*args):
	"""if DEBUG: print args"""
	if DEBUG:
		print args
