#!/usr/bin/python

from gps import *
from math import acos, atan, sqrt, pi
import threading
gpsd = None

MAX_POSITIONS = 20

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
		l = len(self.lastPositions)
		if l < 2:
			return -1
		else:
			start_x, start_y = (0.0, 0.0)
			end_x, end_y = (0.0, 0.0)
			c_start, c_end = 0, 0
			for lat, lon in self.lastPositions:
				if c_start < l/2.0:
					start_x += lon
					start_y += lat
					c_start += 1
				else:
					end_x += lon
					end_y += lat
					c_end += 1
			
			start_x /= c_start
			start_y /= c_start
			end_x /= c_end
			end_y /= c_end
			
			angle = pi/2.0 - atan((end_y-start_y)/(end_x-start_x))
			
			if start_x < end_x:
				return angle
			else:
				return pi + angle				
