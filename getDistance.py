import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

trig = 18
echo = 24

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def distance():
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        startTime = time.time()
        stopTime = time.time()

        #write startTime
        while GPIO.input(echo) == 0:
                startTime = time.time()

        #write time of signal reaching sensor
        while GPIO.input(echo) == 1:
                stopTime = time.time()

        timeElapsed = stopTime - startTime

        #distance equals elapsed time times sonic speed divided by two
        #because the distance is traveled twice
        distance = (timeElapsed * 34300) / 2

        return distance

if __name__ == '__main__':
        try:
                while True:
                        dist = distance()
                        print("%.1f cm" % dist)
                        time.sleep(0.5)

        except KeyboardInterrupt:
                GPIO.cleanup()


