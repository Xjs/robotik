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


#to-do: Ueberlegen wie man aus Sackgassen und aehnlichen Fallen wieder rauskommt (Rueckwaerts fahren und so)

#----------------------NO LONGER NEEDED- left in there for educational purposes---------------------#
#threshold in [m] gibt die Maximaldistanz zu beachtender Objekte aus.
#threshold = 1.5
#bullshitdist in [m] gibt ungefähre Grenze sinnvoller Messung an.
#bullshitdist = 3
#lowpass gibt den maximalen Abstand an, den ein sich Objekt innerhalb zweier Messungen herankommen kann.
#lowpass = 0.2
#averageminimum gives the minimum amound of elements in the average-list for getting a useful result.
#averageminimum = 2
#---------------------------------------------------------------------------------------------------#


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

	def __init__(self):
		#threading.Thread.__init__(self)
		self.watchlistL = []
		self.watchlistR = []
	
	def alarm(self):
		
		alarmL=watchlistL[:1]
		alarmR=watchlistR[:1]
		
		if((watchlistL[:1]-watchlistR[:1])*(watchlistL[:2]-watchlistR[:2]) < 0):
			if(alarmL < alarmR):
				alarmR = alarmR - bias
			if(alarmL > alarmR):
				alarmL = alarmL - bias
		
		
		return (alarmL, alarmR)
	
	def watch(self):
		
		a=distance(0)
		if(a>0):
			self.watchlistL.append(a)
			if (len(self.watchlistL) > measrange):
				self.watchlistL = self.watchlistL[1:]
		b=distance(1)
		if(b>0):
			self.watchlistR.append(b)
			if (len(self.watchlistR) > measrange):
				self.watchlistR = self.watchlistR[1:]
					
	def obstancle(self):
		
		self.watch()
		
		while(len(self.watchlistL) < measrange and len(self.watchlistR) < measrange):
			self.watch()
		
		(L,R) = self.alarm()
		
		if (L > deaththreshold and R > deaththreshold):
		
			while min(L,R) < bullshitdist:
				if (self.watchlistL[-1] > deaththreshold and self.watchlistR[-1] > deaththreshold):
					if (L < R):
						if(L*movefactor > 0.715):
							steer(-L*movefactor)
							##Test
							print("Ich lenke nach Links" , L,-L*movefactor)
						else:
							steer(-0.715)
							##Test
							print("Ich lenke nach Links, maximal" , L, 0.715)
					if (R < L):
						if(R*movefactor > 0.715):
							steer(R*movefactor)
							##Test
							print("Ich lenke nach rechts" , R, R*movefactor)
						else:
							steer(0.715)
							##Test
							print("Ich lenke nach Rechts, maximal" , R, 0.715)
				else:
					drive(-2)
					time.sleep(0.5)
					stop()
					print("Fahr nicht gegen ne Wand du Arsch")
				
				(L,R) = self.alarm()
		else:
			if (L < R):
				steerat(0.715,-1)
				
				##Test
				print("Rückwärts nach links" , L,-L*movefactor)
			if (R < L):
				steerat(-0.715,-1)
				print("Rückwärts nach rechts" , R, R*movefactor)
				
				
