from network.client import Client
from network.datahandler import *

from proto import game_pb2

if __name__ == "__main__":
	handler = DataHandler()
	player = Client(handler)
	player.start(ip = '127.0.0.1', port = 8888)
