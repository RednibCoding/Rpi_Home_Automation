"""
        config.py
        
author:                 Michael Binder
dependencies:   Configparser
description:    Handles loading and saving the "config.ini", needed by the app
"""

from configparser import SectionProxy
import json

from kivy.config import ConfigParser

SECTIONS_WITH_JSON = ('Tabs', 'Buttons')

SECTION_BUTTONS = 'Buttons'
SECTION_NETWORKING = 'Networking'

BUTTON_NAME = 'name'
BUTTON_SWITCHCODE = 'code'
BUTTON_TOOGLE_ON_ALL_OFF = 'toggle-on-all-off'

class Property:

    def __init__(self, section):
        self._dict = {}
        for key in section.keys():
            value = section[key]
            if section.name in SECTIONS_WITH_JSON:
                value = value.replace('\'', '"')
                value = json.loads(value)
            self._dict[key] = value
        print(self._dict)

    def __getitem__(self, item):
        return self._dict[item]

    def __iter__(self):
        yield from self._dict


class Config(ConfigParser):
    def __init__(self, cfg_file):
        super(Config, self).__init__()
        self.file = cfg_file
        self.read(cfg_file)

    def __getitem__(self, item):
        section = super().__getitem__(item)
        return Property(section)

    def get_buttons_with_all_off(self):
        '''Returns an list with all Buttons which have "toggle-on-all-off" set'''
        buttons_with_alloff = []
        for button in self.buttons:
            if button[BUTTON_TOOGLE_ON_ALL_OFF]:
                buttons_with_alloff.append(button)
        return buttons_with_alloff

    def save_file(self, cfg_file):
        '''Saves the Config to the config file'''
        with open(cfg_file, "w") as configfile:
            self.write()
