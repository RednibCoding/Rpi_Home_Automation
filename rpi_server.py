#!/usr/bin/env python3

# execute this script on your raspberry pi
# dependencies: tcp.py


from tcp import Tcp
import RPi.GPIO as gpio
import sys

myTcp=Tcp(port=5000, bufferLen=1024, ip="0.0.0.0")

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
oPins=[None]*4
oPins[0]=27

gpio.setup(oPins[0], gpio.OUT)

for i in range(len(oPins)):
	if oPins[i]:
		gpio.setup(oPins[i], gpio.OUT)

myTcp.bindSocket("0.0.0.0")


def isOutputPinHigh(pin):
    return gpio.input(pin)

print("Server running:")
print("")

try:
	while True:
		msg=myTcp.recvMsg()
		
		if "Button 1" in msg:
			if not isOutputPinHigh(oPins[0]):
				gpio.output(oPins[0], gpio.HIGH)
			elif isOutputPinHigh(oPins[0]):
				gpio.output(oPins[0], gpio.LOW)
		
		elif "Button 2" in msg:
			gpio.output(oPins[0], gpio.LOW)
			
		elif "ALL_OFF" in msg:
			for i in range(len(oPins)):
				if oPins[i]:
					if isOutputPinHigh(oPins[i]):
						gpio.output(oPins[i], gpio.LOW)
			

		print("Incoming message: "+msg)
except KeyboardInterrupt:
	gpio.cleanup()
	print("Exit")

sys.exit()
    



