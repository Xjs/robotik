import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#LEFT
trig = 23
echo = 24

#RIGHT
trig2 = 25
echo2 = 8

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

GPIO.setup(trig2, GPIO.OUT)
GPIO.setup(echo2, GPIO.IN)


def distance(sensor):

        if(sensor==0):
                GPIO.output(trig, True)
                time.sleep(0.00001)
                GPIO.output(trig, False)

                startTime = time.time()
                stopTime = time.time()

                #write startTime
                while GPIO.input(echo) == 0:
                        pass
                startTime = time.time()

                 #write time of signal reaching sensor
                while GPIO.input(echo) == 1:
                        stopTime = time.time()
        else:
                GPIO.output(trig2, True)
                time.sleep(0.00001)
                GPIO.output(trig2, False)

                startTime = time.time()
                stopTime = time.time()

                #write startTime
                while GPIO.input(echo2) == 0:
                        pass
                startTime = time.time()

                 #write time of signal reaching sensor
                while GPIO.input(echo2) == 1:
                        stopTime = time.time()

        timeElapsed = stopTime - startTime

        #distance equals elapsed time times sonic speed divided by two
        #because the distance is traveled twice
        distance = (timeElapsed * 343) / 2

        return distance



