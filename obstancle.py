from getDistance.py import *
from drive.py import *
from math.py import abs
import time

#to-do: Überlegen wie man aus Sackgassen und ähnlichen Fallen wieder rauskommt (Rückwärts fahren und so)
#threshold in [m] gibt die Maximaldistanz zu beachtender Objekte aus.
threshold = 2
bullshitdist = 4
tolerance = 0.005
lowpass = 0.2
measrange = 6
movefactor = 2
averageminimum = 2
deathreshold = 0.3


class watch:

	def __init__(self):
		#threading.Thread.__init__(self)
		self.watchlistL = []
		self.watchlistR = []
	
	def alarm():
		
		averagesL = []
		
		for eins, zwei in zip(self.watchlistL, self.watchlistL[1:]):
			if (abs(eins - zwei) > lowpass and eins < bullshitdist and zwei < bullshitdist)
				averagesL.append((eins+zwei)/2)
				
		averagesR = []
		
		for eins, zwei in zip(self.watchlistR, self.watchlistR[1:]):
			if (abs(eins - zwei) > lowpass and eins < bullshitdist and zwei < bullshitdist)
				averagesR.append((eins+zwei)/2)
		
		alarmL = bullshitdist
		alarmR = bullshitdist
		
		if (averagesL[len(averagesL)-1] < threshold and len(averagesL) > averageminimum)
			
			for eins, zwei in zip(averagesL, averagesL[1:]):
				if (eins < zwei):
					alarmL = bullshitdist
					break
				else:
					alarmL = averagesL[len(averagesL)-1]
		
		if (averagesR[len(averagesR)-1] < threshold and len(averagesR) > averageminimum)
			
			for eins, zwei in zip(averagesR, averagesR[1:]):
				if (eins < zwei):
					alarmR = bullshitdist
					break
				else:
					alarmR = averagesR[len(averagesR)-1]
					
		return (alarmL, alarmR)
	
	def watch():
	
		self.watchlistL.append(distance(0))
		if len(self.watchlistL) > measrange:
			self.watchlistL = self.watchlistL[1:]
			
		b = distance(1)
		self.watchlistR.append(b)
		if len(self.watchlistR) > measrange:
			self.watchlistR = self.watchlistR[1:]
					
	def obstancle():
		
		watch()
		
		while(len(watchlistL) < measrange and len(watchlistR) < measrange):
			watch()
			
		if (watchlistL[len(watchlistL)-1] > deaththreshold and watchlistR[len(watchlistR)-1] > deaththreshold):
			
			(L,R) = alarm()
			
			if (L < R)
				steer(-alarmL*movefactor)
			if (R < L)
				steer(alarmR*movefactor)
		else:
			drive(-2)
			time.sleep(0.5)
			stop()
				
			
			

		
	
	
