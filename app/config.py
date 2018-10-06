
"""
	config.py
	
author:			Michael Binder
dependencies:	Configparser
description:	Handles loading and saving the "config.ini", needed by the app
"""

from kivy.config import ConfigParser

class Config(ConfigParser):
	def __init__(self, cfgFile):
		super(Config, self).__init__()
		self._cfgFile=cfgFile
		self._rpiIp=0
		self._rpiPort=0
		self._remoteCode=0
		self._btnTexts=[None]*7
		self._btnsAllOff=[None]*6
		self._switchCodes=[None]*6
		self._cronEnabled=False
		self._cronTurnOn=0.0
		self._cronTurnOff=0.0
		self._btnsCronOnOff=[None]*6

	def loadFile(self):
		self.read(self._cfgFile)
		# Network
		self._rpiIp=self.get("Network", "Rpi_Ip")
		self._rpiPort=self.get("Network", "Rpi_Port")
		self._remoteCode=self.get("Network", "Remote_Code")
		# Control
		self._btnTexts[1]=self.get("Layout", "btn1")
		self._btnTexts[2]=self.get("Layout", "btn2")
		self._btnTexts[3]=self.get("Layout", "btn3")
		self._btnTexts[4]=self.get("Layout", "btn4")
		self._btnTexts[5]=self.get("Layout", "btn5")
		self._btnTexts[6]=self.get("Layout", "btn6")
		self._btnTexts[0]=self.get("Layout", "btnOff")
		# All Off
		self._btnsAllOff[0]=self.getboolean("All_Off", "btn1AllOff")
		self._btnsAllOff[1]=self.getboolean("All_Off", "btn2AllOff")
		self._btnsAllOff[2]=self.getboolean("All_Off", "btn3AllOff")
		self._btnsAllOff[3]=self.getboolean("All_Off", "btn4AllOff")
		self._btnsAllOff[4]=self.getboolean("All_Off", "btn5AllOff")
		self._btnsAllOff[5]=self.getboolean("All_Off", "btn6AllOff")
		# Switch Codes
		self._switchCodes[0]=self.get("Switch_Codes", "btn1")
		self._switchCodes[1]=self.get("Switch_Codes", "btn2")
		self._switchCodes[2]=self.get("Switch_Codes", "btn3")
		self._switchCodes[3]=self.get("Switch_Codes", "btn4")
		self._switchCodes[4]=self.get("Switch_Codes", "btn5")
		self._switchCodes[5]=self.get("Switch_Codes", "btn6")
		# Cron
		self._cronEnabled=self.getboolean("Cron", "Enabled")
		self._cronTurnOn=self.get("Cron", "Turn_On")
		self._cronTurnOff=self.get("Cron", "Turn_Off")
		# Btn Cron On Off
		self._btnsCronOnOff[0]=self.getboolean("Cron", "btn1CronOnOff")
		self._btnsCronOnOff[1]=self.getboolean("Cron", "btn2CronOnOff")
		self._btnsCronOnOff[2]=self.getboolean("Cron", "btn3CronOnOff")
		self._btnsCronOnOff[3]=self.getboolean("Cron", "btn4CronOnOff")
		self._btnsCronOnOff[4]=self.getboolean("Cron", "btn5CronOnOff")
		self._btnsCronOnOff[5]=self.getboolean("Cron", "btn6CronOnOff")

	def update(self):
		# Network
		self.set("Network", "Rpi_Ip", self._rpiIp)
		self.set("Network", "Rpi_Port", self._rpiPort)
		self.set("Network", "Remote_Code", self._remoteCode)
		# Control
		self.set("Layout", "btn1", self._btnTexts[1])
		self.set("Layout", "btn2", self._btnTexts[2])
		self.set("Layout", "btn3", self._btnTexts[3])
		self.set("Layout", "btn4", self._btnTexts[4])
		self.set("Layout", "btn5", self._btnTexts[5])
		self.set("Layout", "btn6", self._btnTexts[6])
		self.set("Layout", "btnOff", self._btnTexts[0])
		# Buttons All Off
		self.set("All_Off", "btn1AllOff", self._btnsAllOff[0])
		self.set("All_Off", "btn2AllOff", self._btnsAllOff[1])
		self.set("All_Off", "btn3AllOff", self._btnsAllOff[2])
		self.set("All_Off", "btn4AllOff", self._btnsAllOff[3])
		self.set("All_Off", "btn5AllOff", self._btnsAllOff[4])
		self.set("All_Off", "btn6AllOff", self._btnsAllOff[5])
		# Switch Codes
		self.set("Switch_Codes", "btn1", self._switchCodes[0])
		self.set("Switch_Codes", "btn2", self._switchCodes[1])
		self.set("Switch_Codes", "btn3", self._switchCodes[2])
		self.set("Switch_Codes", "btn4", self._switchCodes[3])
		self.set("Switch_Codes", "btn5", self._switchCodes[4])
		self.set("Switch_Codes", "btn6", self._switchCodes[5])
		# Cron
		self.set("Cron", "Enabled", self._cronEnabled)
		self.set("Cron", "Turn_On", self._cronTurnOn)
		self.set("Cron", "Turn_Off", self._cronTurnOff)
		# Btn Cron On Off
		self.set("Cron", "btn1CronOnOff", self._btnsCronOnOff[0])
		self.set("Cron", "btn2CronOnOff", self._btnsCronOnOff[1])
		self.set("Cron", "btn3CronOnOff", self._btnsCronOnOff[2])
		self.set("Cron", "btn4CronOnOff", self._btnsCronOnOff[3])
		self.set("Cron", "btn5CronOnOff", self._btnsCronOnOff[4])
		self.set("Cron", "btn6CronOnOff", self._btnsCronOnOff[5])

	def saveFile(self, cfgFile):
		with open(cfgFile, "w") as configfile:
			self.write()
