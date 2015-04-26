from getDistance import * 
from drive import * 
import time 
from math import *

#-----------------INTRODUCTION-------------------------------------------#
#Principle of work: The latest version of the Mechanised Resistance Autonomous Vehicle(MERAV 5000S) is designed to overcome simple mechanical obstancles like
#Trees, Rocks or, for that matter, boxes, put in MERAVs way by evil enemy fighters, or for test purposes.
#MERAVs sensor-array consists of two ultrasonic devices designed to measure distances to solid objects with great accuracy of about an inch and an angle of measurement of about 15 degrees.
#These sensors are aligned slightly outwards to have little overlap. If an obstancle is located in MERAVs path, it avoids it by steering. To decide the appropriate direction, it compares
#distance data from both sensors and steers towards the bigger distance. To avoid problems with objects right in front of the MERAV 5000 sticks with its steering decision until the
#signal leading towards the opposite side overcomes a certain level, compared to the second sensor. This is necessary to guarantee that the measurement error does not lead to sudden changes
#when facing objects directly in front of MERAV. These could otherwise cause the MERAV 5000 to hit the obstancle rather than avoid it.
#Previous attempts of equipping the MERAV 5000 with intelligent algorithms to distinguish obstancles from false data and taking smart driving-decisions proved to be unstable, and
#have therefore been discarded in favor of this approach, that is more simple, but apparently more effective as well.

#bullshitdist in [m] gibt ungefaere Grenze sinnvoller Messung an.
bullshitdist = 1.5
#measrange gives Number of measurements stored in the watchlist
measrange = 3
#movefactor gives the strength of steering to overcome obstancles. The path-curvature scales linearly with the distance to the obstancle.
movefactor = 2
#deaththreshold gives the minimum distance to an obstancle. If it comes too close, safety is no longer granted (as if it is otherwise) and the car stops.
deaththreshold = 0.3
#bias gives the minimum difference the two sensors have to measure if an obstancle is believed to be on the other side than before. This is to avoid sudden changes,
#uncertainties and eventual death due to hitting obstancles right in front of the car.
bias = 0.05
class Watcher():


	#Init: Creating lists to store sensor-data.
	def __init__(self):
		self.watchlistL = []
		self.watchlistR = []
	
	#alarm: stores data from both sensors into watchlist.
	def alarm(self):
		alarmL=self.watchlistL[-1]
		alarmR=self.watchlistR[-1]
		
		#To prevent the car from unstable motion in front of obstancles, in case the larger distance changes from one site to the other, the difference has to be larger than a certain bias about the size of the error of measurement.
		if((self.watchlistL[-1]-self.watchlistR[-1])*(self.watchlistL[-2]-self.watchlistR[-2]) < 0):
			if(alarmL < alarmR):
				alarmR = alarmR - bias
			if(alarmL > alarmR):
				alarmL = alarmL - bias
		
		return (alarmL, alarmR)
	
	#watch: reads the sensors and fills the watchlist. In case of an improper signal, the maximum meaurement distance bullshitdist is written into the list.
	#The list stores only the last few measurement-points, given by measrange.
	def watch(self):
		a=distance(0)
		if(a>0):
			self.watchlistL.append(a)
			if (len(self.watchlistL) > measrange):
				self.watchlistL = self.watchlistL[1:]
		else:
			self.watchlistL.append(bullshitdist)
		b=distance(1)
		if(b>0):
			self.watchlistR.append(b)
			if (len(self.watchlistR) > measrange):
				self.watchlistR = self.watchlistR[1:]
		else:
			self.watchlistR.append(bullshitdist)
	
	#obstancle: Main routine of obstancle. Fills the watchlists and then reacts to obstancles below the threshold by turning towards the larger distance.
	def obstancle(self):
#		return
		start = time.time()
		
		#watching and waiting until the list is filled up
		self.watch()
		
		while(len(self.watchlistL) < measrange and len(self.watchlistR) < measrange):
			self.watch()
		
		#getting distance-measurements
		(L,R) = self.alarm()
		
		#checking if distance is larger than a minimum-safety-distance. If this is not the case, the car goes backwards.
		if (L > deaththreshold and R > deaththreshold):
			
			#obstancle takes the weel until no object is within the thresholddistance bullshitdist
			while min(L,R) < bullshitdist:
				
				#again checking for safety-distance every measurement-cycle
				if (self.watchlistL[-1] > deaththreshold and self.watchlistR[-1] > deaththreshold):
					
					#turning towards the larger distance. Curvature-radius scales linearly with distance and the gauge-value movefactor
					if (L < R):
						if(L*movefactor > 0.715):
							steer(-L*movefactor) #negative curve radius steers to the right
							##Test
							print("Ich lenke nach rechts" , L,-L*movefactor)
							end = time.time()
							print "this took", end-start
						#Limiting to the maximum value for the steering-servo.
						else:
							steer(-0.715)
							##Test
							print("Ich lenke nach rechts, maximal" , L, 0.715)
							end = time.time()
							print "this took", end-start
					if (R < L):
						if(R*movefactor > 0.715):
							steer(R*movefactor)
							##Test
							print("Ich lenke nach links" , R, R*movefactor)
							end = time.time()
							print "this took", end-start
						else:
							steer(0.715)
							##Test
							print("Ich lenke nach links, maximal" , R, 0.715)
							end = time.time()
							print "this took", end-start
				#going backwards:
				else:
					drive(-2)
					time.sleep(0.5)
					stop()
					print("Fahr nicht gegen ne Wand du Arsch")

				(L,R) = self.alarm()
				self.watch()
		#going backwards:
		else:
			if (L < R):
				steer_at(0.715,-1)

				##Test
				print("Rueckwaerts nach links" , L,-L*movefactor)
			if (R < L):
				steer_at(-0.715,-1)
				print("Rueckwaerts nach rechts" , R, R*movefactor)


if __name__ == "__main__":
	o = Watcher()
	o.obstancle()
