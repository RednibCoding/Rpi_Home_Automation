#!/usr/bin/env python3

"""
    tcp.py

author:     Michael Binder
dependencies:   socket module
description:    Handles Tcp/Ip connections for easier use
"""

from socket import (
    socket,
    AF_INET,
    SOCK_DGRAM
)


# TODO: If i'm not wrong this is an UDP socket.
class Tcp():
    '''Socket helper function'''

    def __init__(self, ip, port, bufferLen):
        # ip="192.168.178.42"
        # port=5000
        # bufferLen=1024
        self._SERVER_IP = ip
        self._PORT = port
        self._SIZE = bufferLen
        self._tcpSocket = socket(AF_INET, SOCK_DGRAM)

    def sendMsg(self, msg):
        data = msg.encode("utf-8")
        self._tcpSocket.sendto(data, (self._SERVER_IP, self._PORT))

    def recvMsg(self):
        (data, addr) = self._tcpSocket.recvfrom(self._SIZE)
        strMsg = data.decode("utf-8")
        return strMsg

    # must only be called by the server app (hostName="0.0.0.0")
    def bindSocket(self):
        # Bind to '0.0.0.0' accepts local and network packages
        self._tcpSocket.bind(('0.0.0.0', self._PORT))
