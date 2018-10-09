#!/usr/bin/env python3

"""
    Rpi Server

author:     Michael Binder
dependencies:   tcp.py, RPi.GPIO, sys, ConfigParser
description:    Establishes a connection via Tcp/Ip in the local network
        and waits for messages sent from the app.
        Then it evaluates those messages and sends them via the connected 433MHz RF-Module
        to the 433MHz receivers (eg. 433MHz outlets)
"""


from configparser import ConfigParser
from logging import (
    Logger,
    StreamHandler
)
import RPi.GPIO as gpio

from tcp import Tcp


OPINS = [27]


def isOutputPinHigh(pin):
    if pin:
        return gpio.input(pin)
    raise ValueError('Pin not set!')


class RpiServer:
    '''Class which manages the IOT server'''

    def __init__(self):
        self.cfg = None
        self.setup_config()
        self.tcp = Tcp(port=5000, bufferLen=1024, ip="0.0.0.0")
        self.tcp.bindSocket()
        self.log = Logger('main')
        self.log.addHandler(StreamHandler())

    def __call__(self):
        self.log.info("Server running:")
        try:
            while True:
                self.log.debug('Waiting for msg')
                msg = self.tcp.recvMsg()

                if "Button 1" in msg:
                    if not isOutputPinHigh(OPINS[0]):
                        gpio.output(OPINS[0], gpio.HIGH)
                    elif isOutputPinHigh(OPINS[0]):
                        gpio.output(OPINS[0], gpio.LOW)

                elif "Button 2" in msg:
                    gpio.output(OPINS[0], gpio.LOW)

                elif "ALL_OFF" in msg:
                    for pin in OPINS:
                        if pin:
                            if isOutputPinHigh(pin):
                                gpio.output(pin, gpio.LOW)

                elif "Cron:" in msg:
                    # Expects to get every config entry in the right order.
                    newMsg = msg.replace("Cron:", "")
                    listMsg = newMsg.split("|")
                    for (value, cfg_entry) in zip(listMsg, self.cfg.cron):
                        self.cfg.cron[cfg_entry] = value
                    self.save_cfg()

                self.log.info("Incoming message: %s", msg)
        except KeyboardInterrupt:
            self.log.info("Exit")

    def __del__(self):
        '''Gets always executet if the instance is destroyed.
        Also if an Exeption happens
        '''
        gpio.cleanup()

    def setup_config(self):
        self.cfg = ConfigParser()
        self.cfg.read("config.ini")
        self.cfg.cron = self.cfg['Cron']

    def save_cfg(self):
        '''saves config'''
        with open("config.ini", 'w') as configfile:
            self.cfg.write(configfile)


def main():
    '''Gets only called when run in an python shell, Ignoring imports'''

    # Setup GPIO'S
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)

    for pin in OPINS:
        if pin:
            gpio.setup(pin, gpio.OUT)
    RpiServer()()


if __name__ == '__main__':
    main()
