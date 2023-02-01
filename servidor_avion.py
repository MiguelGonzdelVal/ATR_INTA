import socket
import sys
from IENA import IENA
import struct
import datetime

def adquisicion_param_avion():
	import __main__
	global __main__
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	server_address = ('172.20.10.5',51000)
	sock.bind(server_address)
	data_size=288
	while True:
		data,address = sock.recvfrom(data_size)
		i = IENA()
		i.unpack(data)
		__main__.V=struct.unpack('iiiddddddddddddd152x',i.payload)[-1]
