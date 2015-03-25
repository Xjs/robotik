from getDistance import *
from drive import *
import time

#to-do: Ueberlegen wie man aus Sackgassen und aehnlichen Fallen wieder rauskommt (Rueckwaerts fahren und so)
#threshold in [m] gibt die Maximaldistanz zu beachtender Objekte aus.
threshold = 2
bullshitdist = 4
tolerance = 0.005
lowpass = 0.2
measrange = 6
movefactor = 2
averageminimum = 2
deathreshold = 0.3


class Watcher():

	def __init__(self):
		#threading.Thread.__init__(self)
		self.watchlistL = []
		self.watchlistR = []
	
	def alarm():
		
		averagesL = []
		
		for eins, zwei in zip(self.watchlistL, self.watchlistL[1:]):
			if (abs(eins - zwei) > lowpass and eins < bullshitdist and zwei < bullshitdist):
				averagesL.append((eins+zwei)/2)
				
		averagesR = []
		
		for eins, zwei in zip(self.watchlistR, self.watchlistR[1:]):
			if (abs(eins - zwei) > lowpass and eins < bullshitdist and zwei < bullshitdist):
				averagesR.append((eins+zwei)/2)
		
		alarmL = bullshitdist
		alarmR = bullshitdist
		
		if (averagesL[len(averagesL)-1] < threshold and len(averagesL) > averageminimum):
			
			for eins, zwei in zip(averagesL, averagesL[1:]):
				if (eins < zwei):
					alarmL = bullshitdist
					break
				else:
					alarmL = averagesL[len(averagesL)-1]
		
		if (averagesR[len(averagesR)-1] < threshold and len(averagesR) > averageminimum):
			
			for eins, zwei in zip(averagesR, averagesR[1:]):
				if (eins < zwei):
					alarmR = bullshitdist
					break
				else:
					alarmR = averagesR[len(averagesR)-1]
					
		return (alarmL, alarmR)
	
	def watch():
	
		self.watchlistL.append(distance(0))
		if (len(self.watchlistL) > measrange):
			self.watchlistL = self.watchlistL[1:]
			
		b = distance(1)
		self.watchlistR.append(b)
		if (len(self.watchlistR) > measrange):
			self.watchlistR = self.watchlistR[1:]
					
	def obstancle():
		
		watch()
		
		while(len(self.watchlistL) < measrange and len(self.watchlistR) < measrange):
			watch()
		
		(L,R) = alarm()
		
		if (self.watchlistL[len(self.watchlistL)-1] > deaththreshold and self.watchlistR[len(self.watchlistR)-1] > deaththreshold):
		
			while(L < bullshitdist or R < bullshitdist):
				
				if (L < R):
					steer(-alarmL*movefactor)
				if (R < L):
					steer(alarmR*movefactor)
				watch()
				
				(L,R) = alarm()
		else:
			drive(-2)
			time.sleep(0.5)
			stop()
				
			
			

		
	
	
