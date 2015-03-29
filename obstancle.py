from getDistance import *
from drive import *
import time
from math import *

#to-do: Ueberlegen wie man aus Sackgassen und aehnlichen Fallen wieder rauskommt (Rueckwaerts fahren und so)
#threshold in [m] gibt die Maximaldistanz zu beachtender Objekte aus.
threshold = 2
bullshitdist = 3
lowpass = 0.2
measrange = 6
movefactor = 2
averageminimum = 2
deaththreshold = 0.3

class Watcher():

	def __init__(self):
		#threading.Thread.__init__(self)
		self.watchlistL = []
		self.watchlistR = []
	
	def alarm(self):
		
		averagesL = []
		
		for eins, zwei in zip(self.watchlistL, self.watchlistL[1:]):
			if (abs(eins - zwei) < lowpass and eins < bullshitdist and zwei < bullshitdist):
				averagesL.append((eins+zwei)/2)
				
		averagesR = []
		
		for eins, zwei in zip(self.watchlistR, self.watchlistR[1:]):
			if (abs(eins - zwei) < lowpass and eins < bullshitdist and zwei < bullshitdist):
				averagesR.append((eins+zwei)/2)
		
		alarmL = bullshitdist
		alarmR = bullshitdist
		
		if (len(averagesL) > averageminimum):
			if(averagesL[-1] < threshold): #list[-1] is the Python way of getting the last element out of a list
	
			
# This treats every increase in average as an outlier! But what if obstacle was only measured for the first time during measurements averaged in zwei?
#				for eins, zwei in zip(averagesL, averagesL[1:]):
#					if (eins < zwei):
				for el1, el2, el3 in zip(averagesL, averagesL[1:], averagesL[2:]):
					if(el1 < el2 and el2 > el3): #this checks for outliers more reliably
						alarmL = bullshitdist
						break
					else:
						alarmL = averagesL[-1]  #not sure about this...
			else:
				print("Halber Bullshit")
		else:
			print("Bullshit hoch 10")
			
		if (len(averagesR) > averageminimum):
			if(averagesR[-1] < threshold):
#				for eins, zwei in zip(averagesR, averagesR[1:]):
#					if (eins < zwei):
				for el1, el2, el3 in zip(averagesR, averagesR[1:], averagesR[2:]):
					if(el1 < el2 and el2 > el3): #this checks for outliers more reliably
						alarmR = bullshitdist
						break
					else:
						alarmR = averagesR[-1]
			else:
				print("Halber Bullshit")
		else:
			print("Bullshit hoch 10")
			
		return (alarmL, alarmR)
	
	def watch(self):
		
		a=distance(0)
		if(a!=-1):
			self.watchlistL.append(a)
			if (len(self.watchlistL) > measrange):
				self.watchlistL = self.watchlistL[1:]
		b=distance(1)
		if(b!=-1):
			self.watchlistR.append(b)
			if (len(self.watchlistR) > measrange):
				self.watchlistR = self.watchlistR[1:]
					
	def obstancle(self):
		
		self.watch()
		
		while(len(self.watchlistL) < measrange and len(self.watchlistR) < measrange):
			self.watch()
		
		(L,R) = self.alarm()
		
		if (self.watchlistL[-1] > deaththreshold and self.watchlistR[-1] > deaththreshold):
		
			while min(L,R) < bullshitdist:
				if (self.watchlistL[-1] > deaththreshold and self.watchlistR[-1] > deaththreshold):
					if (L < R):
						steer(-L*movefactor)
						##Test
						print("Ich lenke nach Links" , L,-L*movefactor)
					if (R < L):
						steer(R*movefactor)
						print("Ich lenke nach rechts" , R, R*movefactor)
					self.watch()
				else:
					drive(-2)
					time.sleep(0.5)
					stop()
					print("Fahr nicht gegen ne Wand du Arsch")
				
				(L,R) = self.alarm()
		else:
			drive(-2)
			time.sleep(0.5)
			stop()
			print("Fahr nicht gegen ne Wand du Arsch")
