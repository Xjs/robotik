import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#LEFT, RIGHT
trig = [18, 22]
echo = [24, 23]

for t, e in zip(trig, echo):
	GPIO.setup(t, GPIO.OUT)
	GPIO.setup(e, GPIO.IN)

def distance(sensor):
	GPIO.output(trig[sensor], True)
	time.sleep(0.00001)
	GPIO.output(trig[sensor], False)
	
	startTime = time.time()
	stopTime = time.time()
	
	#write startTime
	while GPIO.input(echo[sensor]) == 0:
	startTime = time.time()
	
	 #write time of signal reaching sensor
	while GPIO.input(echo[sensor]) == 1:
			stopTime = time.time()
	
	timeElapsed = stopTime - startTime
	
	#distance equals elapsed time times sonic speed divided by two
	#because the distance is traveled twice
	distance = (timeElapsed * 343) / 2
	
	return distance
