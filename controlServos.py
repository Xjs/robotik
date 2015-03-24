from RPIO import PWM
import time

servo1 = PWM.Servo()
servo2 = PWM.Servo()

BASE = 1500
RIGHT = (1800-1500) 
LEFT = (1170-1500)

FORWARD = (1952-1500)
BACK = (1000-1500)


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

if __name__ == '__main__':
	test()
