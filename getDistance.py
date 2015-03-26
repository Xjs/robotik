import RPi.GPIO as GPIO
import time

MAX_DIST = 4.
SPEED_OF_SOUND = 343.

GPIO.setmode(GPIO.BCM)

#LEFT, RIGHT
trig = [18, 27]
echo = [24, 23]

for t, e in zip(trig, echo):
	GPIO.setup(t, GPIO.OUT)
	GPIO.setup(e, GPIO.IN)

def distance(sensor):
	time.sleep(0.01) # give the sensor some time to relax
	GPIO.output(trig[sensor], True)
	time.sleep(0.00001)
	GPIO.output(trig[sensor], False)
	
	startTime = time.time()
	stopTime = time.time()
	st = startTime
	
	#write startTime
	while GPIO.input(echo[sensor]) == 0 and startTime-st < 2.*MAX_DIST/SPEED_OF_SOUND:
		startTime = time.time()
	
	 #write time of signal reaching sensor
	while GPIO.input(echo[sensor]) == 1 and stopTime-startTime < 2.*MAX_DIST/SPEED_OF_SOUND:
		stopTime = time.time()
	
	timeElapsed = stopTime - startTime
	
	#distance equals elapsed time times sonic speed divided by two
	#because the distance is traveled twice
	distance = (timeElapsed * 343) / 2
	if distance > 4:
		return -1.0
	else:
		return distance
