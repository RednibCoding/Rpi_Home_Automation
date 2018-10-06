#!/usr/bin/env python3


"""
	main.py
	
author:			Michael Binder
dependencies:	kivy, tcp, config, picontroller.kv
description:	Main client app.
				Via this app, the user can controll the Raspberry Pi
				that is running the server script (rpi_server.py)
				This file must be named "main.py" in order for kivy to work
"""

import kivy
kivy.require('1.0.6') # replace with current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup

from tcp import Tcp
from config import Config


class ClientApp(TabbedPanel):
	def __init__(self):
		super(ClientApp, self).__init__()
		self._cfg=Config("config.ini")
		self._cfg.loadFile()
		self.cfgToInputBoxes()
		rpiIp=self._cfg._rpiIp
		rpiPort=int(self._cfg._rpiPort)
		self._tcp=Tcp(port=rpiPort, bufferLen=1024, ip=rpiIp)

	def updateSettings(self):
		self.inputBoxesToCfg()
		self._cfg.update()
		self._cfg.saveFile("config.ini")
		self._cfg.loadFile()
		self.cfgToInputBoxes()
	
	# button click events
	def on_btn1_click(self):
		msg=self.ids.btn1SwitchCode.text
		self._tcp.sendMsg(msg)

	def on_btn2_click(self):
		msg=self.ids.btn2SwitchCode.text
		self._tcp.sendMsg(msg)

	def on_btn3_click(self):
		msg=self.ids.btn3SwitchCode.text
		self._tcp.sendMsg(msg)

	def on_btn4_click(self):
		msg=self.ids.btn4SwitchCode.text
		self._tcp.sendMsg(msg)

	def on_btn5_click(self):
		msg=self.ids.btn5SwitchCode.text
		self._tcp.sendMsg(msg)

	def on_btn6_click(self):
		msg=self.ids.btn6SwitchCode.text
		self._tcp.sendMsg(msg)
		
	def on_btn7_click(self):
		msg="ALL_OFF:"
		states=str(self.ids.btn1AllOff.active)+"|"
		states=states+str(self.ids.btn2AllOff.active)+"|"
		states=states+str(self.ids.btn3AllOff.active)+"|"
		states=states+str(self.ids.btn4AllOff.active)+"|"
		states=states+str(self.ids.btn5AllOff.active)+"|"
		states=states+str(self.ids.btn6AllOff.active)
		msg=msg+states
		self._tcp.sendMsg(msg)
		
	def on_btnSaveConfig_click(self):
		self.updateSettings()
		popup = Popup(title='Settings',
		content=Label(text='Saved!'), size_hint=(None, None), size=(410, 410))
		popup.open()
		rpiIp=self._cfg._rpiIp
		rpiPort=int(self._cfg._rpiPort)
		self._tcp=Tcp(port=rpiPort, bufferLen=1024, ip=rpiIp)
		
	def on_btnSaveCron_click(self):
		self.on_btnSaveConfig_click()
		self.sendCronToPi()
		
		
	def sendCronToPi(self):
		msg="Cron:"
		states=str(self.ids.cronEnabled.active)+"|"
		states=states+str(self.ids.cronTurnOn.text)+"|"
		states=states+str(self.ids.cronTurnOff.text)+"|"
		states=states+str(self.ids.btn1CronOnOff.active)+"|"
		states=states+str(self.ids.btn2CronOnOff.active)+"|"
		states=states+str(self.ids.btn3CronOnOff.active)+"|"
		states=states+str(self.ids.btn4CronOnOff.active)+"|"
		states=states+str(self.ids.btn5CronOnOff.active)+"|"
		states=states+str(self.ids.btn6CronOnOff.active)
		msg=msg+states
		self._tcp.sendMsg(msg)


	def inputBoxesToCfg(self):
		# Network
		self._cfg._rpiIp=self.ids.rpiIp.text
		self._cfg._rpiPort=self.ids.rpiPort.text
		self._cfg._remoteCode=self.ids.remoteCode.text
		# Button Text Control
		self._cfg._btnTexts[1]=self.ids.btn1.text
		self._cfg._btnTexts[2]=self.ids.btn2.text
		self._cfg._btnTexts[3]=self.ids.btn3.text
		self._cfg._btnTexts[4]=self.ids.btn4.text
		self._cfg._btnTexts[5]=self.ids.btn5.text
		self._cfg._btnTexts[6]=self.ids.btn6.text
		self._cfg._btnTexts[0]=self.ids.btn7.text
		# Button Text Layout
		self._cfg._btnTexts[1]=self.ids.btn1Layout.text
		self._cfg._btnTexts[2]=self.ids.btn2Layout.text
		self._cfg._btnTexts[3]=self.ids.btn3Layout.text
		self._cfg._btnTexts[4]=self.ids.btn4Layout.text
		self._cfg._btnTexts[5]=self.ids.btn5Layout.text
		self._cfg._btnTexts[6]=self.ids.btn6Layout.text
		# Buttons All Off
		self._cfg._btnsAllOff[0]=self.ids.btn1AllOff.active
		self._cfg._btnsAllOff[1]=self.ids.btn2AllOff.active
		self._cfg._btnsAllOff[2]=self.ids.btn3AllOff.active
		self._cfg._btnsAllOff[3]=self.ids.btn4AllOff.active
		self._cfg._btnsAllOff[4]=self.ids.btn5AllOff.active
		self._cfg._btnsAllOff[5]=self.ids.btn6AllOff.active
		# Button Switch Codes
		self._cfg._switchCodes[0]=self.ids.btn1SwitchCode.text
		self._cfg._switchCodes[1]=self.ids.btn2SwitchCode.text
		self._cfg._switchCodes[2]=self.ids.btn3SwitchCode.text
		self._cfg._switchCodes[3]=self.ids.btn4SwitchCode.text
		self._cfg._switchCodes[4]=self.ids.btn5SwitchCode.text
		self._cfg._switchCodes[5]=self.ids.btn6SwitchCode.text
		# Cron
		self._cfg._cronEnabled=self.ids.cronEnabled.active
		self._cfg._cronTurnOn=self.ids.cronTurnOn.text
		self._cfg._cronTurnOff=self.ids.cronTurnOff.text
		# Btn Cron On Off
		self._cfg._btnsCronOnOff[0]=self.ids.btn1CronOnOff.active
		self._cfg._btnsCronOnOff[1]=self.ids.btn2CronOnOff.active
		self._cfg._btnsCronOnOff[2]=self.ids.btn3CronOnOff.active
		self._cfg._btnsCronOnOff[3]=self.ids.btn4CronOnOff.active
		self._cfg._btnsCronOnOff[4]=self.ids.btn5CronOnOff.active
		self._cfg._btnsCronOnOff[5]=self.ids.btn6CronOnOff.active

	def cfgToInputBoxes(self):
		# Network
		self.ids.rpiIp.text=self._cfg._rpiIp
		self.ids.rpiPort.text=self._cfg._rpiPort
		self.ids.remoteCode.text=self._cfg._remoteCode
		# Button Text Control
		self.ids.btn1.text=self._cfg._btnTexts[1]
		self.ids.btn2.text=self._cfg._btnTexts[2]
		self.ids.btn3.text=self._cfg._btnTexts[3]
		self.ids.btn4.text=self._cfg._btnTexts[4]
		self.ids.btn5.text=self._cfg._btnTexts[5]
		self.ids.btn6.text=self._cfg._btnTexts[6]
		self.ids.btn7.text=self._cfg._btnTexts[0]
		# Button Text Layout
		self.ids.btn1Layout.text=self._cfg._btnTexts[1]
		self.ids.btn2Layout.text=self._cfg._btnTexts[2]
		self.ids.btn3Layout.text=self._cfg._btnTexts[3]
		self.ids.btn4Layout.text=self._cfg._btnTexts[4]
		self.ids.btn5Layout.text=self._cfg._btnTexts[5]
		self.ids.btn6Layout.text=self._cfg._btnTexts[6]
		# Buttons All Off
		self.ids.btn1AllOff.active=self._cfg._btnsAllOff[0]
		self.ids.btn2AllOff.active=self._cfg._btnsAllOff[1]
		self.ids.btn3AllOff.active=self._cfg._btnsAllOff[2]
		self.ids.btn4AllOff.active=self._cfg._btnsAllOff[3]
		self.ids.btn5AllOff.active=self._cfg._btnsAllOff[4]
		self.ids.btn6AllOff.active=self._cfg._btnsAllOff[5]
		# Lables Buttons All Off
		self.ids.lbl1AllOff.text="Button "+self.ids.btn1.text
		self.ids.lbl2AllOff.text="Button "+self.ids.btn2.text
		self.ids.lbl3AllOff.text="Button "+self.ids.btn3.text
		self.ids.lbl4AllOff.text="Button "+self.ids.btn4.text
		self.ids.lbl5AllOff.text="Button "+self.ids.btn5.text
		self.ids.lbl6AllOff.text="Button "+self.ids.btn6.text
		# Button Switch Codes
		self.ids.btn1SwitchCode.text=self._cfg._switchCodes[0]
		self.ids.btn2SwitchCode.text=self._cfg._switchCodes[1]
		self.ids.btn3SwitchCode.text=self._cfg._switchCodes[2]
		self.ids.btn4SwitchCode.text=self._cfg._switchCodes[3]
		self.ids.btn5SwitchCode.text=self._cfg._switchCodes[4]
		self.ids.btn6SwitchCode.text=self._cfg._switchCodes[5]
		# Lables Button Switch Codes
		self.ids.lblBtn1SwitchCode.text="Button "+self.ids.btn1.text
		self.ids.lblBtn2SwitchCode.text="Button "+self.ids.btn2.text
		self.ids.lblBtn3SwitchCode.text="Button "+self.ids.btn3.text
		self.ids.lblBtn4SwitchCode.text="Button "+self.ids.btn4.text
		self.ids.lblBtn5SwitchCode.text="Button "+self.ids.btn5.text
		self.ids.lblBtn6SwitchCode.text="Button "+self.ids.btn6.text
		# Cron
		self.ids.cronEnabled.active=self._cfg._cronEnabled
		self.ids.cronTurnOn.text=self._cfg._cronTurnOn
		self.ids.cronTurnOff.text=self._cfg._cronTurnOff
		# Buttons Cron On Off
		self.ids.btn1CronOnOff.active=self._cfg._btnsCronOnOff[0]
		self.ids.btn2CronOnOff.active=self._cfg._btnsCronOnOff[1]
		self.ids.btn3CronOnOff.active=self._cfg._btnsCronOnOff[2]
		self.ids.btn4CronOnOff.active=self._cfg._btnsCronOnOff[3]
		self.ids.btn5CronOnOff.active=self._cfg._btnsCronOnOff[4]
		self.ids.btn6CronOnOff.active=self._cfg._btnsCronOnOff[5]
		# Lables Cron On Off
		self.ids.lbl1CronOnOff.text="Button "+self.ids.btn1.text
		self.ids.lbl2CronOnOff.text="Button "+self.ids.btn2.text
		self.ids.lbl3CronOnOff.text="Button "+self.ids.btn3.text
		self.ids.lbl4CronOnOff.text="Button "+self.ids.btn4.text
		self.ids.lbl5CronOnOff.text="Button "+self.ids.btn5.text
		self.ids.lbl6CronOnOff.text="Button "+self.ids.btn6.text



class PiControllerApp(App):
    def build(self):
        return ClientApp()

if __name__ == '__main__':
    PiControllerApp().run()
