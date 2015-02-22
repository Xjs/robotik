import serial
import pigpio
import time
from array import array

def sendMessage(deg=0.0, speed=0.0):
	TXD = 23
	RXD = 24

	pi = pigpio.pi()

	pi.bb_serial_read_open(RXD, 9600, 8) #8 is the bits per word i.e. one byte - alternatively 80 bits == one message?

	pi.set_mode(TXD,pigpio.OUTPUT)
	pi.wave_clear()

	
	prep_message = array('B',[deg,speed]) #create an array of unsigned chars 
	message = array('B', [255, prep_message, 0]) #create an array started off by 0xFF, followed by the message in machine values and ended with 0x00

	
	pi.wave_add_serial(TXD, 9600, message)
	wid = wave_create()

	while True:
		try:
			pi.wave_send_repeat(wid)
		except Exception, e:
			time.sleep(1)
			continue
