#!/usr/bin/env python3

# execute this script on your raspberry pi
# dependencies: tcp.py


from tcp import Tcp
import RPi.GPIO as gpio

myTcp=Tcp(port=5000, bufferLen=1024)

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
pin=27
gpio.setup(pin, gpio.OUT)

myTcp.bindSocket("0.0.0.0")

state=False

while True:
    msg=myTcp.recvMsg()

    if "Button 1" in msg:
		if not state:
			gpio.output(pinNum. gpio.HIGH)
			state=True
		elif state:
			gpio.output(pinNum. gpio.LOW)
			state=False			
    elif "Button 2" in msg:
        gpio.output(pinNum. gpio.LOW)
    print(msg)

sys.exit()
