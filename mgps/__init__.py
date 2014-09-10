#!/usr/bin/python

from gps import *
from math import acos, atan, sqrt, pi
from helpers import angle_to_north
from time import sleep
import threading
gpsd = None

MAX_POSITIONS = 20
N_AVERAGES = 3

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
	def __init__(self, n_averages=N_AVERAGES):	
		self.poller = GPSPoller()
		self.latitude = -1
		self.longitude = -1
		self.altitude = -1
		self.lastPositions = []
		self.poller.start()
		self.n_averages = n_averages
	
	def getRawPosition(self):
		if gpsd.fix.mode == MODE_NO_FIX:
			return None
		return (gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude)
	
	def getPosition(self):
		positions = []
		lat, lon, alt = 0.0, 0.0, 0.0
		for i in xrange(self.n_averages):
			try:
				n_lat, n_lon, n_alt = self.getRawPosition()
			except TypeError:
				return None
			lat += n_lat
			lon += n_lon
			alt += n_alt
			sleep(0.1)
		
		lat, lon, alt = (value/self.n_averages for value in (lat, lon, alt))
		
		self.latitude = lat
		self.longitude = lon
		self.altitude = alt
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
			
			return angle_to_north((start_x, start_y), (end_x, end_y))
	
