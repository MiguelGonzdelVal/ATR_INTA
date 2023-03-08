# from mmap import MADV_DODUMP
import socket
import sys
import IENA
import struct
import time
import datetime
import pandas
# Create a UDP socket
def envio_datos(LW,LWC,ACC_RATE):
	"""Send icing cloud parameters to the airplane acquisition system

	Args:
		LW (bool): Liquid Water presence
		LWC (float): Liquid Water Content
		ACC_RATE (float): IAR (mm/min)
	"""	
	

	LW_O=0.0
	MVD =20.0
	ACC =LW
	ACC_O=0.0
	ACC_THK = 0.0
	
	actual = datetime.datetime.timestamp(datetime.datetime.now())
	referencia=datetime.datetime.timestamp(datetime.datetime(2022, 1, 1, 0, 0, 0, 0))
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	conexiones= pandas.read_csv('DATOS_CONEXIONES.csv',sep=';',index_col='ELEMENTO')
	IP=conexiones['IP'].loc['FOD']
	Puerto=conexiones['PUERTO'].loc['FOD']
	server_address = (IP, Puerto)
	i = IENA.IENA()
	i.key = 80
	# i.key = struct.pack('i', 80)
	i.sequence = 1
	#i.endfield = 0xDEAD
	i.keystatus = 0
	i.status = 1
	i.timeusec = int((actual-referencia)*1e6)
	#print(i.timeusec)
	#i.payload = struct.pack('xfxfxfxfxfxfxfxfxfx', LW, LW_O, LWC,MVD,0.0,ACC,ACC_O,ACC_THK,ACC_RATE)
	i.payload = struct.pack('11d184x',0,0, 1, LW, LW_O,LWC,MVD,ACC,ACC_O,ACC_THK,ACC_RATE)
	print(len(i.pack())-288)
	#while len(i.pack())!=288:
		#i.payload+=struct.pack('x')
	message=i.pack()
	
	print(i.size)
	try:
		sent = sock.sendto(message, server_address)
		
	except:print('no se enviaron datos')

	sock.close()
