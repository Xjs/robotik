from getDistance.py import *
from steer.py import *
from stop.py import *
from drive.py import *

threshold = 2

def obstacle():
	while((a = distance(0) < threshold) or (b = distance(1) < threshold)):
			if(a<b):
				steer(0.715)
			else:
				steer(-0.715)
	
	stop()
