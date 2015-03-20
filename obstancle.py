from getDistance.py import *
from steer.py import *
from stop.py import *
from drive.py import *

#to-do: Überlegen wie man aus Sackgassen und ähnlichen Fallen wieder rauskommt (Rückwärts fahren und so)
#threshold in [m] gibt die Maximaldistanz zu beachtender Objekte aus.
threshold = 2
bullshitdist = 6
runs = 3

#runs ist die Zahl der Messvorgänge-1 über die gemittelt wird um eine Fehlerarme Distanz zu berechnen.


# def average(initial,sensor):
	# dist = initial/runs
	
	# #Mittelung über mehrere Messvorgänge. Fällt ein Wert aus dem Rahmen ( a,b > threshold ) wird er ignoriert.
	# for i in range(runs-1):
		# s = distance(sensor)
		# #Wenn ein zu großer Wert gemessen wird, geht der initiale Wert ein weiteres mal in die Messung ein.
		# if (s < bullshitdist):
			# dist = dist + s/runs
		# else:
			# dist = dist + initial/runs
	# stop()
	# return dist

def obstacle():
	a = distance(a,0);
	b = distance(b,1);
	
	# if((a < threshold) or (b < threshold)):
		# a = average(0)
		# b = average(1)
	
	#Permanente Überprüfung ob a,b unter der Maximaldistanz anzeigen
		while((a < threshold) or (b < threshold)):
			
		#Links/Rechts sind die gemittelten Werte der Entfernungsmessung der Sensoren. a/b speichern die aktuelle Entfernungsmessung.
	
			if(a<b):
				steer(0.715)
			else:
				steer(-0.715)
		# a = average(a,0)
		# b = average(a,1)
		
		a = distance(0);
		b = distance(1);
		
		stop()
		
		steer(0.0)
