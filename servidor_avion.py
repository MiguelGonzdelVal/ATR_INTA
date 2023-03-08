import socket
import sys
from IENA import IENA
import struct
import datetime
class ATR_data(object):
        def __init__(self):
                self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                
        def adquisicion_param_avion(self):
                """Funcion que consiste en cargar la IP y puerto del HIDS para importar los datos
                Los guarda en el __main__

                """	
                import __main__
                global __main__
                import pandas as pd
                import time
                
                
                
                Conectado = False
                while not Conectado:
                        conexiones= pd.read_csv('DATOS_CONEXIONES.csv',sep=';',index_col='ELEMENTO')
                        IP=conexiones['IP'].loc['HIDS']
                        Puerto=conexiones['PUERTO'].loc['HIDS']
                        
                        server_address = (IP,Puerto)
                        try:
                                self.sock.bind(server_address)
                                Conectado=True
                        except:
                                print(f'Direccion {server_address[0]} invalida')
                                time.sleep(10)
                data_size=288
                file=open('campos_IENA.txt','r')
                campos=file.readlines()
                file.close()
                while True:
                        data,address = self.sock.recvfrom(data_size)
                        i = IENA()
                        i.unpack(data)
                        datos=struct.unpack('3i25d56x',i.payload)
                        TOTAL={}
                        for j,campo in enumerate(campos):TOTAL.update({campo[:-1]:datos[j+3]})
                        __main__.V=TOTAL['IAS']
                        print(TOTAL,__main__.V)

