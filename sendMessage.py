import serial
import pigpio
import time
import signal
import sys
from struct import pack
from array import array

#def handler(signum, frame):
#	print "Exiting..."
#	pi.bb_serial_read_close(RXD)
#	pi.wave_delete(wid)
#	pi.stop()
#	sys.exit(0)

def sendMessage(deg=0.0, speed=0.0):
	TXD = 17
	RXD = 22

	pi = pigpio.pi()

	pi.bb_serial_read_open(RXD, 9600, 8) #8 is the bits per word i.e. one byte - alternatively 80 bits == one message?

	pi.set_mode(TXD,pigpio.OUTPUT)
	pi.wave_clear()

	
	#prep_message = array('B',[deg,speed]) #create an array of unsigned chars 
	#message = array('B', [255, prep_message, 0]) #create an array started off by 0xFF, followed by the message in machine values and ended with 0x00

	prep_message = bytes()
	num = [255.0, deg,speed, 0.0]
	prep_message = prep_message.join((pack('f', val) for val in num))
	
	pi.wave_add_serial(TXD, 9600, prep_message)
	wid = pi.wave_create()

#	signal.signal(signal.SIGINT,handler)

	while True:
		try:
			pi.wave_send_once(wid)
		except Exception, e:
			time.sleep(1)
			continue


if __name__ == "__main__":
	sendMessage()
