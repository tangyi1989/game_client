#!/usr/bin/env python
#coding:utf-8

from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, error

from packet import *
from utils.utils import *
from proto import game_pb2

class Client():
	'''
	客户端类
	'''
	
	def __init__(self, handler):
		self.handler = handler
		self.factory = gameClientFactory(handler)
		

	def start(self, **params):
		self.connector = reactor.connectTCP(params['ip'], params['port'], self.factory)
		reactor.run()
	
	def stop(self):
		pass

	def sendData(self, cmd, data):
		print data
		#self.factory.protocol.transport.write(encode(cmd, data))
		
	
class gameClientFactory(ClientFactory):
        def __init__(self, handler):
                self.protocol = gameClientProtocol(self)
		self.handler = handler

        def startedConnecting(self, connector):
                log("Connecting to server....")

        def buildProtocol(self, addr):
                return self.protocol

        def clientConnectionFailed(self, connector, reason):
                print reason.getErrorMessage()

        def clientConnectionLost(self, connector, reason):
                print reason.getErrorMessage()
                try:
                        log("Disconnection from game server")
                except error.ReactorNotRunning:
               		pass


class gameClientProtocol(LineReceiver):
        def __init__(self, factory):
                self.factory = factory

        def connectionMade(self):
                '''
                这里开始去发送账号姓名去请求登陆
                '''
		login_packet = game_pb2.Login()
        	login_packet.name = 'tang'
        	login_packet.password = 'tangwanwan'
        	#self.transport.write(encode(101, login_packet))
		self.sendLine(encode(101, login_packet))
                log("Connecton established to server")

        def dataReceived(self, data):
                '''
                这里开始将接收到的数据传递给protocol去解析,
                并且对解析到的数据进行handle
                '''
                log("Recevie data from server")
                log(" -> " + data)
		self.factory.handler.handle(data)

       	def sendData(self, encodeData):
                self.sendLine(encodeData)
