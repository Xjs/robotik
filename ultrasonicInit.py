from getDistance import *
from time import sleep

# This is an initialisation skript for running before starting the car.
# Due to technical properties of the ultrasonic sensors, they seem to need 
# some working time to run accurately.

def init():
	#Check left sensor
	left = distance(0)
	print("left: ", left)
	
	#Check right sensor
	right = distance(1)
	print("right: ", right)
	
if __name__ == "__main__":
	for i in range(500):
		init()
		time.sleep(0.02) #wait 20 ms because sensors can only make one measurement every 20 ms
	
	#this takes 10 s  
