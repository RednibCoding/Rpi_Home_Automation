#!/usr/bin/env python3


import logging

from rfDevice import RFDevice

print(" ----------- Sending data -----------")

pinTX=27

rfdevice = RFDevice(pinTX)
rfdevice.enable_tx()

tmpCode=1361

print("Code: "+str(tmpCode))
             
success=rfdevice.tx_code(tmpCode)
rfdevice.cleanup()