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
#from configParser import ConfigParser

from rfDevice import RFDevice


myTcp=Tcp(port=5000, bufferLen=1024, ip="0.0.0.0")
myTcp.bindSocket("0.0.0.0")


gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
oPins=[None]*1
oPins[0]=27

gpio.setup(oPins[0], gpio.OUT)





def isOutputPinHigh(pin):
    return gpio.input(pin)

"""
cfg=ConfigParser()
cfg.read("config.ini")
cronEnabled=cfg.getboolean("Cron", "enabled")
cronTurnOn=cfg.get("Cron", "turn_on")
cronTurnOff=cfg.get("Cron", "turn_off")
btn1cronOnOff=cfg.get("Cron", "btn1crononoff")
btn2cronOnOff=cfg.get("Cron", "btn2crononoff")
btn3cronOnOff=cfg.get("Cron", "btn3crononoff")
btn4cronOnOff=cfg.get("Cron", "btn4crononoff")
btn5cronOnOff=cfg.get("Cron", "btn5crononoff")
btn6cronOnOff=cfg.get("Cron", "btn6crononoff")
"""

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
		
		if "Button 1" in msg:
			if not isOutputPinHigh(oPins[0]):
				gpio.output(oPins[0], gpio.HIGH)
			elif isOutputPinHigh(oPins[0]):
				gpio.output(oPins[0], gpio.LOW)
		
		elif "Button 2" in msg:
			gpio.output(oPins[0], gpio.LOW)
			
		elif "ALL_OFF" in msg:
			newMsg=msg.replace("ALL_OFF:", "")
			listMsg=newMsg.split("|")
			for entry in listMsg:
				print(entry)
						
		elif "Cron:" in msg:
			newMsg=msg.replace("Cron:", "")
			listMsg=newMsg.split("|")
			cfg.set("Cron", "enabled", listMsg[0])
			cfg.set("Cron", "turn_on", listMsg[1])
			cfg.set("Cron", "turn_off", listMsg[2])
			cfg.set("Cron", "btn1crononoff", listMsg[3])
			cfg.set("Cron", "btn2crononoff", listMsg[4])
			cfg.set("Cron", "btn3crononoff", listMsg[5])
			cfg.set("Cron", "btn4crononoff", listMsg[6])
			cfg.set("Cron", "btn5crononoff", listMsg[7])
			cfg.set("Cron", "btn6crononoff", listMsg[8])
			
			with open("config.ini", 'w') as configfile:
				cfg.write(configfile)
				
		else:
			rfdevice = RFDevice(17)
			rfdevice.enable_tx()
			success=rfdevice.tx_code(int(msg))
			rfdevice.cleanup()

except KeyboardInterrupt:
	gpio.cleanup()
	print("Exit")

sys.exit()
    



