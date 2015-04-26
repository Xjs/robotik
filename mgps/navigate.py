#!/usr/bin/python

from __future__ import division
from math import sin, cos, sqrt, acos, atan2, pi
from helpers import *
from sympy import Line

RADIUS = 0.5 # meters (this is a dummy value)

# I changed these values back, otherwise I'd have to filter atan2 data in a complicated way. Better change steer.
CCW = 1
CW = -1

 # TODO: measure what distance between line and GPS position can be deemed
 # a deviation from our path
THRESHOLD = 0.00001

class Navigator:
	"""Uses a GPSTracker object. Provides a method to navigate directly to a
	given target point and one to check if the car is still on a given track"""
	def __init__(self, tracker):
		# Tracker be a mgps.GPSTracker object
		self.tracker = tracker
		self.radius = RADIUS
	
	def setRadius(self, r):
		"""Set curve radius used for internal calculations"""
		# convert to angular distance
		self.radius = r
		
	def navigate(self, target, dummy_position = None, dummy_orientation = None):
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
		if dummy_position is not None:
			my_latitude, my_longitude = dummy_position
		else:
			my_latitude, my_longitude = self.tracker.getPosition()
		# switch lat/lon
		me = (my_longitude, my_latitude)
		if dummy_orientation is not None:
			orientation = dummy_orientation
		else:
			orientation = self.tracker.getOrientation()
		
		debug_print("my_long ", my_longitude)
		debug_print("my_lat ", my_latitude)
		
		# Calculate the distances from my position to the midpoints of the 
		# two circles I can drive. The longitude distance has to be adjusted
		# depending on the latitude
		d_lat = to_deg(r*sin(orientation)/EARTH_RADIUS)
		d_lon = to_deg(r*cos(orientation)/EARTH_RADIUS)/(cos(to_rad(my_latitude)))
		
		# switch lat/lon
		midpoint_a = (my_longitude + d_lon, my_latitude - d_lat)
		midpoint_b = (my_longitude - d_lon, my_latitude + d_lat)
		distance_a = distance(midpoint_a, target_point)
		distance_b = distance(midpoint_b, target_point)
		
		# choose the circle that is closer to the target. This defines the
		# driving direction.
		# fun is used later to pick out the correct angle because this depends
		# too on the driving direction, and the angles are oriented
		if distance_a < distance_b:
			direction = CW
			midpoint = midpoint_a
			fun = max
		else:
			direction = CCW
			midpoint = midpoint_b
			fun = min
		
		# the intution (see also: documentation) is: We lay tangents on the
		# circle and I drive until one of the tangent points, then I steer
		# straight
		# Use trigonometry (a rectangular triangle with my position, the 
		# midpoint and the tangent point as corners) to find out which angle
		# I have to drive
		gamma = angle_to_north(midpoint, target_point)
		alpha = acos(sqrt(d_lat**2+d_lon**2)/distance(midpoint, target_point))
		# the epsilons are the angles to north of the two tangent points
		epsilons = [normalize(gamma+alpha), normalize(gamma-alpha)]
		
		# oriented angles are the angles I have to drive to the two tangent 
		# points
		oriented_angles = [normalize(orientation + direction * pi/2) - eps for eps in epsilons]
		
		candidates = []
		
		debug_print("me ", me)
		debug_print("target ", target)
		debug_print("midpoint ", midpoint)
		debug_print("oriented_angles ", oriented_angles)
		debug_print("direction ", direction)
		
		# normalize the angles so that they have the correct signage,
		# append them to the candidate list
		for a, eps in zip(oriented_angles, epsilons):
			if sign(a) != direction:
				a += direction*2*pi
				debug_print("a is now ", a)
			# calculate the coordinates of the tangent point in order to
			# have a starting point for the straight line
			d_lat = -to_deg(r*sin(eps)/EARTH_RADIUS)
			d_lon = -to_deg(r*cos(eps)/EARTH_RADIUS)/(cos(to_rad(my_latitude)))
			midpoint_x, midpoint_y = midpoint
			start_x = midpoint_x + d_lon
			start_y = midpoint_y + d_lat
			candidates.append((a, (start_y, start_x))) # TODO: start?
		#debug_print("start ", start)
		
		# choose the smaller angle
		angle, start = fun(candidates)
		debug_print("start ", start)
		return ((direction, angle, r), (start, target))
	
	def on_track(self, line):
		"""Are we still on track (that is, is our distance to the given line
		small enough? If not, better re-navigate"""
		if line is None:
			return False
		else:
			line = Line(*line)
			return line.distance(self.tracker.getPosition()) < THRESHOLD
