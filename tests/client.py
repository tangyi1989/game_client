import time
import packet
import socket
from proto import game_pb2


def hex_str(s):
    return ":".join("{0:x}".format(ord(c)) for c in s)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 8888))

    login_packet = game_pb2.Login()
    login_packet.name = 'tang'
    login_packet.password = 'tangwanwan'

    buf = packet.pack(101, login_packet)
    print  hex_str(buf)
    sock.send(buf)

    time.sleep(10)