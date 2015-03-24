from RPIO import PWM

servo = PWM.Servo()

BASE = 1500
RIGHT = (1800-1500) 
LEFT = (1170-1500)

FORWARD = (1952-1500)
BACK = (1000-1500)


def test():
	# Set servo on GPIO17 (BCM) to (1.2ms)
	servo.set_servo(17, 1600)

	# Set servo on GPIO17 (BCM) (2.0ms)
	servo.set_servo(17, 1200)

	# Clear servo on GPIO17
	servo.stop_servo(17)
	
	# Set servo on GPIO22 (BCM) to (1.2ms)
	servo.set_servo(17, 1600)

	# Set servo on GPIO22 (BCM) (2.0ms)
	#servo.set_servo(17, 1200)

	# Clear servo on GPIO22
	servo.stop_servo(17)

if __name__ == '__main__':
	test()
