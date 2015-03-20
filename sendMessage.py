import serial
import pigpio
import time
import signal
import sys
import serial
from struct import pack
from array import array

def parity(c):
    return sum([ord(c) & (1 << i) > 0 for i in range(8)])
   	
def checksum(string):
	result = ''
	for c in string:
		if parity(c) % 2 == 0:
			appendix = '1'
		else
			appendix = '0'
		result.append(appendix)

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

	pi.set_mode(TXD,pigpio.OUTPUT)


	
	pigpio.exceptions = False
	pi.bb_serial_read_close(RXD)
	pigpio.exceptions = True

	pi.bb_serial_read_open(RXD, 9600, 8) #8 is the bits per word i.e. one byte - alternatively 80 bits == one message?

	
	pi.wave_clear()

	
	#prep_message = array('B',[deg,speed]) #create an array of unsigned chars 
	#message = array('B', [255, prep_message, 0]) #create an array started off by 0xFF, followed by the message in machine values and ended with 0x00

	prep_message = bytes()
	num = [deg,speed]
	strings = [pack('f', val) for val in num]
	checksums = [pack('c', int(''.join('0b0000', checksum(string)))) for string in strings]
	prep_message = bytes.join(bytes.join(tuple) for tuple in zip(strings, checksums))
	for i in range(len(prep_message)):
		if prep_message[i] == '\xff':
			prep_message[i] = '\xfe'
	prep_message = bytes().join([pack('c', chr(255)),prep_message,pack('c', chr(0))])
	print repr(prep_message)
	
	pi.wave_add_serial(TXD, 9600, prep_message)
	wid = pi.wave_create()

   #	signal.signal(signal.SIGINT,handler)

	#pi.wave_send_once(wid)

	start = time.time()
	runtime = 300


	while (time.time()-start) < runtime:
		try:
			pi.wave_send_once(wid)
			pi.wave_delete(wid)

			pi.wave_add_serial(TXD, 9600, prep_message)

			while pi.wave_tx_busy():
				pass

			wid = pi.wave_create()

			(count, data) = pi.bb_serial_read(RXD)
			if (data != ''):
				print repr(data)

  		except Exception, e:
  			time.sleep(1)
  			continue
	
	pi.wave_delete(wid)
	pi.bb_serial_read_close(RXD)
	pi.stop()
	sys.exit(0)

#-----------------------------------

#	port = serial.Serial("/dev/ttyAMA0",baudrate=9600)
#	port.write(prep_message)

if __name__ == "__main__":
	sendMessage()
