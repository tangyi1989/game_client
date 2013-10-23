#!/usr/bin/env python
#coding:utf-8

from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, error

from gui.dialogs import alertMessageDialog

from packet import *

class Client():
    '''
    客户端类
    '''
    def __init__(self, handler):
        self.handler = handler
        self.factory = gameClientFactory(handler)
		
    def start(self, **params):
        self.connector = reactor.connectTCP(params['ip'], params['port'], self.factory)

    def sendData(self, cmd, data):
        print data
		#self.factory.protocol.transport.write(encode(cmd, data))

class gameClientFactory(ClientFactory):
    def __init__(self, handler):
        self.protocol = gameClientProtocol(self)
        self.handler = handler

    def startedConnecting(self, connector):
        print ("Connecting to server....")

    def buildProtocol(self, addr):
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        errorMsg = reason.getErrorMessage().split(':')
        alertMessageDialog('Unable to connect to server: ' + errorMsg[1] + errorMsg[2], 'An error occured')
        print reason.getErrorMessage()

    def clientConnectionLost(self, connector, reason):
        print reason.getErrorMessage()
        try:
            print ("Disconnection from game server")
        except error.ReactorNotRunning:
            pass


class gameClientProtocol(LineReceiver):
        def __init__(self, factory):
            self.factory = factory

        def connectionMade(self):
            '''
            这里开始去发送账号姓名去请求登陆
            '''
            print ("Connecton established to server")

        def dataReceived(self, data):
            '''
            这里开始将接收到的数据传递给protocol去解析,
            并且对解析到的数据进行handle
            '''
            print ("Recevie data from server")
            print (" -> " + data)
            self.factory.handler.handle(data)

        def sendData(self, encodeData):
            self.sendLine(encodeData)

