from RPIO import PWM
import time

servo1 = PWM.Servo()
servo2 = PWM.Servo()

BASE = 1500
RIGHT = (1800-1500) 
LEFT = (1170-1500)

FORWARD = (1952-1500)
BACK = (1000-1500)


def steer(float deg):
	#Sets steering degree from -1 == hard left to 1 == hard right
	if(deg < -1 || deg > 1):
		return
	
	elif (deg < 0)
		servo1.set_servo(17, BASE + (-deg)*LEFT)
		
	elif (deg > 0):
		servo1.set_servo(17, BASE + deg*RIGHT)
		
	elif (deg == 0):
		servo1.set_servo(17, BASE)
		
def drive(float speed):
	#Sets engine to drive at a speed between -1 == full throttle backwards and 
	#1 == full throttle forwards
	if(speed < -1 || speed > 1)
		return
		
	elif (speed < 0)
		servo2.set_servo(22, BASE + (-speed)*BACK)
	
	elif (speed > 0)
		servo2.set_servo(22, BASE + speed*FORWARD)
	
	elif (speed == 0)
		servo2.set_servo(22, BASE)

def test():
	# Set servo on GPIO17 (BCM) to (1.2ms)
	servo1.set_servo(17, 1600)
	
	time.sleep(2)

	# Set servo on GPIO17 (BCM) (2.0ms)
	servo1.set_servo(17, 1200)

	time.sleep(2)

	# Clear servo on GPIO17
	servo1.stop_servo(17)
	
	# Set servo on GPIO22 (BCM) to (1.2ms)
	servo2.set_servo(22, 1600)

	time.sleep(2)

	# Set servo on GPIO22 (BCM) (2.0ms)
	#servo.set_servo(17, 1200)

	# Clear servo on GPIO22
	servo2.stop_servo(22)
	
def test2():
	steer(0.5)
	steer(-0.5)
	drive(0.2)

if __name__ == '__main__':
	test2()
