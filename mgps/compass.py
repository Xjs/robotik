#!/usr/bin/python

import smbus
import time
from math import atan2, pi

BUS = 1
ADDR = 0x1e
SCALE = 0.92

class Compass:
	def read_byte(self, adr):
		return bus.read_byte_data(self.address, adr)
	
	def read_word(self, adr):
		high = bus.read_byte_data(self.address, adr)
		low = bus.read_byte_data(self.address, adr+1)
		val = (high << 8) + low
		return val
	
	def read_word_2c(self, adr):
		val = read_word(adr)
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else:
			return val
	
	def write_byte(self, adr, value):
		bus.write_byte_data(self.address, adr, value)
	 
	def __init__(self, bus=BUS, address=ADDR, scale=SCALE):
		self.bus = smbus.SMBus(bus)
		self.address = address
		self.scale = scale
		
	def initialize_compass(self):
		self.write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
		self.write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
		self.write_byte(2, 0b00000000) # Continuous sampling
		
	def set_offset(self, x_offset, y_offset, angle_offset):
		self.x_offset = x_offset
		self.y_offset = y_offset
		self.angle_offset = angle_offset
		
	def calibrate(self):
		self.initialize_compass()
		
		min_x = 0
		max_x = 0
		min_y = 0
		max_y = 0
		
		for i in xrange(500):
			x = read_word_2c(3)
			y = read_word_2c(7)
			z = read_word_2c(5)

			if x < min_x:
				min_x = x
				
			if y < min_y:
				min_y = y
			
			if x > max_x:
				max_x = x
			
			if y > max_y:
				max_y = y
			
			time.sleep(0.1)
			
			x_offset = (max_x + min_x) / 2.0
			y_offset = (max_y + min_y) / 2.0
			
			print "\n\n_________________________________________________"
			print "Turn", i
			print "min_x: ", min_x
			print "min_y: ", min_y
			print "max_x: ", max_x
			print "max_y: ", max_y
			
			print "x offset: ", x_offset
			print "y offset: ", y_offset
	
	def getOrientation(self):
		self.initialize_compass()
		
		x = (read_word_2c(3) - self.x_offset) * self.scale
		y = (read_word_2c(7) - self.y_offset) * self.scale
		z = read_word_2c(5) * self.scale
		
		bearing = (atan2(y, x) - angle_offset)%(2*pi)
		bearing = 2*pi - bearing # we want the clockwise angle between north and the compass
		
		return bearing
