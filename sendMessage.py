import serial
from array import array

def sendMessage(deg=0.0, speed=0.0):

        prep_message = array('B',[deg,speed]) #create an array of unsigned chars 

        message = array('B', [255, prep_message, 0]) #create an array started off by 0xFF, followed by the message in machine values and ended with 0x00

        port = serial.Serial("/dev/ttyAMA0", baudrate=9600) #originally 9600UL

        port.write(message)

