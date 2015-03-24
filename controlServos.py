from RPIO import PWM

servo = PWM.Servo()

BASE = 1500
RIGHT = (1800-1500) 
LEFT = (1170-1500)

FORWARD = (1952-1500)
BACK = (1000-1500)

# Set servo on GPIO17 (BCM) to 1200µs (1.2ms)
servo.set_servo(17, 1600)

# Set servo on GPIO17 to 2000µs (2.0ms)
servo.set_servo(17, 2000)

# Clear servo on GPIO17
servo.stop_servo(17)
