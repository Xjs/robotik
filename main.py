#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from mgps import *
import time
import drive.py

tracker = GPSTracker()





if __name__ == '__main__':
	# GPS-Position bekommen
	curPos = tracker.getPosition
	time.sleep(2)
	while True:
		if curPos == tracker.getPosition:	#car stands still
			# Entweder: (Re-)Initialisierung – geradeausfahren, Orientierung holen (Kompass koennen wir glaub ich nicht vertrauen), kreiseln, bis man drauf zuschaut, 			  anfangen, geradeaus zu fahren
			start = time.time()
			drive(5)			#drive for 5m
			while (time.time() - start) < 3:	#while driving (ca. 3 s) save positions to tracker
				tracker.getPosition
			orientation = tracker.getOrientation()
			#check if orientation is correct
			#if so: drive for approximate number of meters until destination
			#if not: use steer.py to correct orientation
		 
		else: #car is moving
		# Oder: Wir fahren noch
		# 	immer mal wieder Position updaten
			tracker.getPosition()
		# 	mit der Linie vergleichen, und wenn wir zu sehr abweichen, mal wieder von vorn
		# 	Hindernis? Wenn ja: Ausweich-Subroutine und dann von vorn
	
# Ausweich-Subroutine: Lenk solange vom Hindernis weg, bis es nicht mehr da ist
# Wenn es nicht weggeht oder auf beiden Seiten eines gemessen wird… vielleicht rückwärts fahren?
