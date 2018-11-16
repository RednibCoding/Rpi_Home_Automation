#!/usr/bin/env python3

"""
	Rpi Server
	
author:		Michael Binder
dependencies:	tcp.py, RPi.GPIO, sys
description:	Establishes a connection via Tcp/Ip in the local network 
		and waits for messages sent from the app.
		Then it evaluates those messages and sends them via the connected 433MHz RF-Module
		to the 433MHz receivers (eg. 433MHz outlets)
"""

from tcp import Tcp
import RPi.GPIO as gpio
import sys

from rfDevice import RFDevice


myTcp=Tcp(port=5000, bufferLen=1024, ip="0.0.0.0")
myTcp.bindSocket("0.0.0.0")



def isOutputPinHigh(pin):
    return gpio.input(pin)


print("Server running:")
print("")

rfdevice = RFDevice(17)
rfdevice.enable_tx()
success=rfdevice.tx_code(1361)
rfdevice.cleanup()

try:
	while True:
		msg=myTcp.recvMsg()
		print("")
		print("Incoming message: "+msg)
		print("")
		
		# transmit the actual code received from the app via rf module		
		rfdevice = RFDevice(17)
		rfdevice.enable_tx()
		success=rfdevice.tx_code(int(msg))
		rfdevice.cleanup()

except KeyboardInterrupt:
	gpio.cleanup()
	print("Exit")

sys.exit()
    



