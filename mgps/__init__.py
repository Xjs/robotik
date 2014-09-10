#!/usr/bin/python

from gps import *
from math import acos, sqrt, pi
import threading
gpsd = None

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
		if len(self.lastPositions) > 5:
			self.lastPositions = self.lastPositions[1:]
		return position
	
	def getOrientation(self):
		try:
			a = self.lastPositions[-2]
			b = self.lastPositions[-1]
			# TODO: use more than two positions to get a triangle
		except IndexError:
			return -1
		
		x2, x1 = a
		y2, y1 = b
		
		a = y2 - x2
		b = y1 - x1
		c = sqrt(a**2+b**2)
		
		if y1 == x1:
			if y2 < x2:
				return pi
			elif y2 > x2:
				return 0
		
		if y2 == x2:
			if y1 < x1:
				return 1.5 * pi
			elif y1 > x1:
				return 0.5 * pi
			else:
				return -1
		
		if y1 > x1:
			if y2 > x2:
				return acos(a/c)
			else:
				return 0.5 * pi + acos(a/c)
		else:
			if y2 > x2:
				return 1.5 * pi + acos(a/c)
			else:
				return pi + acos(a/c)
				
