#!/usr/bin/env python3

# main client app
# this file must be named "main.py" in order for kivy to work

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

	# button click events
	def on_btn1_click(self):
		myMessage="Button 1 clicked"
		self._tcp.sendMsg(myMessage)

	def on_btn2_click(self):
		myMessage="Button 2 clicked"
		self._tcp.sendMsg(myMessage)

	def on_btn3_click(self):
		myMessage="Button 3 clicked"
		self._tcp.sendMsg(myMessage)

	def on_btn4_click(self):
		myMessage="Button 4 clicked"
		self._tcp.sendMsg(myMessage)

	def on_btn5_click(self):
		myMessage="Button 5 clicked"
		self._tcp.sendMsg(myMessage)

	def on_btn6_click(self):
		myMessage="Button 6 clicked"
		self._tcp.sendMsg(myMessage)

	def on_btn7_click(self):
		myMessage="Button 7 clicked"
		self._tcp.sendMsg(myMessage)

	def on_btn8_click(self):
		myMessage="Button 8 clicked"

	def on_btn9_click(self):
		myMessage="Button 9 clicked"

	def on_btn10_click(self):
		myMessage="Button 10 clicked"

	def on_btn11_click(self):
		myMessage="Button 11 clicked"

	def on_btn12_click(self):
		myMessage="Button 12 clicked"
		
	def on_btn13_click(self):
		myMessage="Button 13 clicked"
		
	def on_btnSaveConfig_click(self):
		self.inputBoxesToCfg()
		self._cfg.update()
		self._cfg.saveFile("test.ini")

		popup = Popup(title='Warning',
		content=Label(text='Restart neccesary'), size_hint=(None, None), size=(400, 400))
		popup.open()

	# helper
	
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
		self._cfg._btnTexts[1]=self.ids.btn8.text
		self._cfg._btnTexts[2]=self.ids.btn9.text
		self._cfg._btnTexts[3]=self.ids.btn10.text
		self._cfg._btnTexts[4]=self.ids.btn11.text
		self._cfg._btnTexts[5]=self.ids.btn12.text
		self._cfg._btnTexts[6]=self.ids.btn13.text
		# Button Switch Codes
		self._cfg._switchCodes[0]=self.ids.btn1SwitchCode.text
		self._cfg._switchCodes[1]=self.ids.btn2SwitchCode.text
		self._cfg._switchCodes[2]=self.ids.btn3SwitchCode.text
		self._cfg._switchCodes[3]=self.ids.btn4SwitchCode.text
		self._cfg._switchCodes[4]=self.ids.btn5SwitchCode.text
		self._cfg._switchCodes[5]=self.ids.btn6SwitchCode.text
		# Lables Button Switch Codes
		self.ids.btn1.text=self.ids.lblBtn1SwitchCode.text
		self.ids.btn2.text=self.ids.lblBtn2SwitchCode.text
		self.ids.btn3.text=self.ids.lblBtn3SwitchCode.text
		self.ids.btn4.text=self.ids.lblBtn4SwitchCode.text
		self.ids.btn5.text=self.ids.lblBtn5SwitchCode.text
		self.ids.btn6.text=self.ids.lblBtn6SwitchCode.text
		# Cron
		self._cfg._cronEnabled=self.ids.cronEnabled.active
		self._cfg._cronTurnOn=self.ids.cronTurnOn.text
		self._cfg._cronTurnOff=self.ids.cronTurnOff.text

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
		self.ids.btn8.text=self._cfg._btnTexts[1]
		self.ids.btn9.text=self._cfg._btnTexts[2]
		self.ids.btn10.text=self._cfg._btnTexts[3]
		self.ids.btn11.text=self._cfg._btnTexts[4]
		self.ids.btn12.text=self._cfg._btnTexts[5]
		self.ids.btn13.text=self._cfg._btnTexts[6]
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



class PiControllerApp(App):
    def build(self):
        return ClientApp()

if __name__ == '__main__':
    PiControllerApp().run()
