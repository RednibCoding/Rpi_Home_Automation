#!/usr/bin/env python3

import signal
import sys
import time

from rfDevice import RFDevice

print(" ----------- Receiving data -----------")

pinRX=17

rfdevice = None

def onExit(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, onExit)
rfdevice = RFDevice(pinRX)
rfdevice.enable_rx()
timestamp = None
print("Listening for codes on GPIO " + str(pinRX))

while True:
	if rfdevice.rx_code_timestamp != timestamp:
		timestamp = rfdevice.rx_code_timestamp
		print(str(rfdevice.rx_code))

	time.sleep(0.01)
	
rfdevice.cleanup()
