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
from logging import getLogger
import json

import kivy
from kivy.app import App
from kivy.uix.gridlayout import (
    GridLayout,
    ReferenceListProperty
)
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import (
    TabbedPanel,
    TabbedPanelItem,
)

from tcp import Tcp
from config import Config
from buttons import (
    RfButton,
    WifiButton,
)
from expections import ButtonConfigEntryError


KIVY_VERSION = '1.0.6'  # replace with current kivy version !

RFBUTTON_TYPE = 'rfbutton'
WIFIBUTTON_TYPE = 'wifibutton'


class ClientApp(TabbedPanel):
    def __init__(self):
        kivy.require(KIVY_VERSION)
        super(ClientApp, self).__init__(do_default_tab=False)
        self.cfg = Config("config.ini")
        self.build_view()
        self.log = getLogger()

    def restore_default(self):
        '''Restore default config'''
        with open('default.cfg', 'rb') as defaultcfg:
            with open('config.ini', 'wb') as cfg:
                cfg.write(defaultcfg.read(-1))
        self.__init__()

    def save_view(self):
        '''save view to config'''
        save_cfg = {}
        for tab in self.get_tab_list():
            pass

    def build_view(self):
        '''Build view'''
        # Remove tabs
        self.clear_tabs()

        # Add Tabs from config
        for tab_key in self.cfg['Tabs']:
            tab_cfg = self.cfg['Tabs'][tab_key]

            # Tab
            tpi = TabbedPanelItem(**tab_cfg)

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
                # Only add button if its the right tab
                if buttoncfg['tab'] == tab_key:
                    # Create right button object
                    if buttoncfg['type'] == RFBUTTON_TYPE:
                        button = RfButton(**buttoncfg)
                    elif buttoncfg['type'] == WIFIBUTTON_TYPE:
                        button = WifiButton(**buttincfg)
                    else:
                        raise ButtonConfigEntryError('Invalid button type for button {}'.format(button_key))
                    gl.add_widget(button)

            # Add Tab to View
            self.add_widget(tpi)

    def on_btnSaveCron_click(self):
        self.on_btnSaveConfig_click()
        self.sendCronToPi()

    def sendCronToPi(self):
        msg = "Cron:"
        states = str(self.ids.cronEnabled.active)+"|"
        states = states+str(self.ids.cronTurnOn.text)+"|"
        states = states+str(self.ids.cronTurnOff.text)+"|"
        states = states+str(self.ids.btn1CronOnOff.active)+"|"
        states = states+str(self.ids.btn2CronOnOff.active)+"|"
        states = states+str(self.ids.btn3CronOnOff.active)+"|"
        states = states+str(self.ids.btn4CronOnOff.active)+"|"
        states = states+str(self.ids.btn5CronOnOff.active)+"|"
        states = states+str(self.ids.btn6CronOnOff.active)
        msg = msg+states
        self._tcp.sendMsg(msg)


class PiControllerApp(App):
    def build(self):
        return ClientApp()


if __name__ == '__main__':
    PiControllerApp().run()
