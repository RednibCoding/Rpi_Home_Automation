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
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
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
from views.edit import EditView


KIVY_VERSION = '1.0.6'  # replace with current kivy version !

RFBUTTON_TYPE = 'rfbutton'
WIFIBUTTON_TYPE = 'wifibutton'
SPECIALBUTTON_TYPE = 'specialbutton'


class ClientApp(TabbedPanel):
    def __init__(self):
        self.tabs = {}
        self.log = getLogger()
        kivy.require(KIVY_VERSION)
        super(ClientApp, self).__init__(do_default_tab=False)
        self.cfg = Config("config.ini")
        self.build_view()

    def restore_default(self):
        '''Restore default config'''
        with open('default.cfg', 'rb') as defaultcfg:
            with open('config.ini', 'wb') as cfg:
                cfg.write(defaultcfg.read())
        self.__init__()

    def build_view(self):
        '''Build view'''
        self.log.info('Building view...')
        # Remove tabs
        self.clear_tabs()
        self.clear_widgets()

        # Add Tabs from config
        for tab_key in self.cfg['Tabs']:
            tab_cfg = self.cfg['Tabs'][tab_key]

            # Tab
            tpi = TabbedPanelItem(**tab_cfg)
            self.tabs[tab_key] = tpi
            # Add Tab to View
            self.add_widget(tpi)

            # ScrollView
            sw = ScrollView()
            tpi.add_widget(sw)

            # Grid Layout
            fl = FloatLayout()
            sw.add_widget(fl)

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
                    elif buttoncfg['specialbutton'] == SPECIALBUTTON_TYPE:
                        pass
                    else:
                        raise ButtonConfigEntryError('Invalid button type for button {}'.format(button_key))
                    fl.add_widget(button)


        # Add edit Tab
        edit = EditView(self)
        self.add_widget(edit.tpi)

        # Select first tab
        self.switch_to(self.tab_list[1])


class PiControllerApp(App):
    def build(self):
        return ClientApp()


if __name__ == '__main__':
    PiControllerApp().run()
