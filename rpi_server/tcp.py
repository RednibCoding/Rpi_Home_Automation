#!/usr/bin/env python3

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM

class Tcp():
    def __init__(self, ip, port, bufferLen):
        # ip="192.168.178.42"
        # port=5000
        # bufferLen=1024
        self._SERVER_IP=ip
        self._PORT=port
        self._SIZE=bufferLen
        self._tcpSocket=socket( AF_INET, SOCK_DGRAM )

    def sendMsg(self, msg):
        data=msg.encode("utf-8")
        self._tcpSocket.sendto(data, (self._SERVER_IP, self._PORT))

    def recvMsg(self):
        (data, addr)=self._tcpSocket.recvfrom(self._SIZE)
        strMsg=data.decode("utf-8")
        return strMsg

    # must only be called by the server app (hostName="0.0.0.0")
    def bindSocket(self, hostName):
        hostName=gethostbyname(hostName)
        self._tcpSocket.bind((hostName, self._PORT))