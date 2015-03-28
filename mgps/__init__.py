#!/usr/bin/python

from gps import *
from math import acos, sqrt, pi
import numpy
import threading
gpsd = None

MAX_POSITIONS = 10

class GPSPoller(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global gpsd
		gpsd = gps(mode = WATCH_ENABLE)
		self.current_value = None
		self.running = True
	
	def run(self):
		global gpsd
		while self.running:
			gpsd.next()
			
class GPSTracker:
	def __init__(self):	
		self.poller = GPSPoller()
		self.latitude = -1
		self.longitude = -1
		self.altitude = -1
		self.lastPositions = []
		self.poller.start()
	
	def getPosition(self):
		if gpsd.fix.mode == MODE_NO_FIX:
			return None
		self.latitude = gpsd.fix.latitude
		self.longitude = gpsd.fix.longitude
		self.altitude = gpsd.fix.altitude
		position = (self.latitude, self.longitude)
		self.lastPositions.append(position)
		if len(self.lastPositions) > MAX_POSITIONS:
			self.lastPositions = self.lastPositions[1:]
		return position
	
	def getOrientation(self):
		l = len(lastPositions)
		if l < 2:
			return -1
		else:
			xs = (x for (x,y) in lastPositions)
			ys = (y for (x,y) in lastPositions)
			slope, _ = numpy.polyfit(xs, ys, 1)
			angle = pi/2.0 - atan(slope)
			start, end = (0.0, 0.0)
			c_start, c_end = 0, 0
			for x, _ in lastPositions:
				if c_start < l/2.0:
					start += x
					c_start += 1
				else:
					end += x
					c_end += 1
			start /= c_start
			end /= c_end
			if start > end:
				return angle
			else:
				return 2*pi + angle				
		