#!/usr/bin/python

from __future__ import division
from math import sin, cos, sqrt, acos, atan2, pi
from helpers import *

RADIUS = 0.5 # meters (this is a dummy value)

# I changed these values back, otherwise I'd have to filter atan2 data in a complicated way. Better change steer.
CCW = 1
CW = -1

 # TODO: measure what distance between line and GPS position can be deemed
 # a deviation from our path
THRESHOLD = 0.00001

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
		# switch lat/lon
		target_point = (t_longitude, t_latitude)
		my_latitude, my_longitude = self.tracker.getPosition()
		# switch lat/lon
		me = (my_longitude, my_latitude)
		orientation = self.tracker.getOrientation()
		print("my_long ", my_longitude)
		print("my_lat ", my_latitude)
		# TODO: Does the following always work, did I understand the trig correctly?
		d_lat = to_deg(r*sin(orientation)/EARTH_RADIUS)
		d_lon = to_deg(r*cos(orientation)/EARTH_RADIUS)/(cos(to_rad(my_latitude)))
		
		# switch lat/lon
		midpoint_a = (my_longitude + d_lon, my_latitude - d_lat)
		midpoint_b = (my_longitude - d_lon, my_latitude + d_lat)
		distance_a = distance(midpoint_a, target_point)
		distance_b = distance(midpoint_b, target_point)
		if distance_a < distance_b:
			direction = CW
			midpoint = midpoint_a
			fun = max
		else:
			direction = CCW
			midpoint = midpoint_b
			fun = min
		print("midpoint ", midpoint)		
		gamma = angle_to_north(midpoint, target_point)
		alpha = acos(sqrt(d_lat**2+d_lon**2)/distance(midpoint, target_point))
		epsilons = [normalize(gamma+alpha), normalize(gamma-alpha)]
		
		oriented_angles = [normalize(orientation + direction * pi/2) - eps for eps in epsilons]
		
		candidates = []
		
		print("me ", me)
		print("target ", target)
		print("midpoint ", midpoint)
		print("oriented_angles ", oriented_angles)
		print("direction ", direction)

		
		for a, eps in zip(oriented_angles, epsilons):
			if sign(a) != direction:
				a += direction*2*pi
			d_lat = -to_deg(r*sin(eps)/EARTH_RADIUS)
			d_lon = -to_deg(r*cos(eps)/EARTH_RADIUS)/(cos(to_rad(my_latitude)))
			midpoint_x, midpoint_y = midpoint
			start_x = midpoint_x + d_lon
			start_y = midpoint_y + d_lat
			candidates.append((a, (start_y, start_x))) # TODO: start?
		#print("start ", start)
		
		angle, start = fun(candidates)
		print("start ", start)
		return ((direction, angle, r), (start, target))
	
	def on_track(self, line):
		"""Are we still on track? If not, better re-navigate"""
		if line is None:
			return False
		else:
			return (distance(line, self.tracker.getPosition()) < 0.00001)# TRESHOLD)
