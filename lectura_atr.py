#archivo de un subproceso que leera los datos de vuelo (temperatura y airspeed y los guardara en el programa´

import socket
import sys
import IENA
import struct
import time
import datetime


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('234.0.0.1', 1024)
data,adress = sock.recvfrom(4096)
print(data.decode)
i = IENA()
i.unpack(rec_payload[0x2a:])
