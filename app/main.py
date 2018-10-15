#!/usr/bin/env python3


"""
        main.py
        
author:                 Michael Binder
dependencies:   kivy, tcp, config, picontroller.kv
description:    Main client app.
                                Via this app, the user can controll the Raspberry Pi
                                that is running the server script (rpi_server.py)
                                This file must be named "main.py" in order for kivy to work
"""

from collections import defaultdict
import json

import kivy
kivy.require('1.0.6') # replace with current kivy version !
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout, ReferenceListProperty
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup

from tcp import Tcp
from config import Config
from buttons import RfButton


class ClientApp(TabbedPanel):
        def __init__(self):
                super(ClientApp, self).__init__()
                self.cfg = Config("config.ini")
                self.build_view()

                #rpiIp = self.cfg._rpiIp
                #rpiPort = int(self.cfg._rpiPort)
                #self._tcp = Tcp(port=rpiPort, bufferLen=1024, ip=rpiIp)

        def restore_default(self):
            '''Restore default config'''
            with open('default.cfg', 'rb') as defaultcfg:
                with open('config.ini', 'wb') as cfg:
                    cfg.write(defaultcfg.read(-1))
            self.__init__()

        def save_view(self):
            '''save view to config'''
            for tab in self.get_tab_list():
                pass

        def build_view(self):
            '''Build view'''
            # Remove tabs
            for tab in self.get_tab_list():
                self.remove_widget(tab)

            # Add Tabs from config
            for tab_key in self.cfg['Tabs']:
                tab = self.cfg['Tabs'][tab_key]
                # Tab
                tpi = TabbedPanelItem()
                tpi.text = tab['text']
                tpi.id = tab['id']

                # ScrollView
                sw = ScrollView()
                tpi.add_widget(sw)

                # Grid Layout
                gl = GridLayout()
                sw.add_widget(gl)
                gl.id = 'gridLayout'
                gl.cols = 2
                gl.size_hint = (1, 1)
                gl.size = gl.parent.size
                gl.pos = gl.parent.pos
                gl.height = gl.minimum_height

                # Add Buttons
                for button_key in self.cfg['Buttons']:
                    buttoncfg = self.cfg['Buttons'][button_key]
                    if buttoncfg['tab'] == tab_key:
                        button = RfButton(buttoncfg['code'])
                        button.id = buttoncfg['id']
                        button.text = buttoncfg['text']
                        button.text_size = buttoncfg['text_size']
                        button.halign = buttoncfg['halign']
                        gl.add_widget(button)
                
                # Add to Tab

                # Add Tab to View
                self.add_widget(tpi)

        def updateSettings(self):
                self.inputBoxesToCfg()
                self.cfg.update()
                self.cfg.saveFile("config.ini")
                self.cfg.loadFile()
                self.cfgToInputBoxes()
        
        def on_btnSaveConfig_click(self):
                self.updateSettings()
                popup = Popup(title='Settings',
                content=Label(text='Saved!'), size_hint=(None, None), size=(410, 410))
                popup.open()
                rpiIp=self.cfg._rpiIp
                rpiPort=int(self.cfg._rpiPort)
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


class PiControllerApp(App):
    def build(self):
        return ClientApp()

if __name__ == '__main__':
    PiControllerApp().run()
