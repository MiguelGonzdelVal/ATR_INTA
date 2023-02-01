import socket
import sys
from IENA import IENA
import struct
import datetime
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = ('192.168.1.34',51000)
def adquisicion_param_avion():
	import __main__
	sock.bind(server_address)
	data_size=288
	while True:
		data,address = sock.recvfrom(data_size)
		i = IENA()
		print(i.unpack(data))
		print(i.key)
		
		print(datetime.datetime.fromtimestamp(i._getPacketTime()))
		__main__.V=struct.unpack('iiiddddddddddddd152x',i.payload)[-1]
		
		

