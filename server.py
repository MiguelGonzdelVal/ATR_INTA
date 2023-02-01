import socket
import sys
import IENA
import struct
import pandas as pd
# Create a UDP socket
sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 50000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
i = IENA.IENA()
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(
        len(data), address))
    print(i.unpack(data))

    inputs=struct.unpack('fffffffff',i.payload)
    nombres=['LW','LW_O','LWC','MVD','_','ACC','ACC_O','ACC_THK','ACC_RATE']
    datos = []
    for indice in range(len(inputs)):
        datos.append([nombres[indice],inputs[indice]])
    
    Resultado=pd.DataFrame(data=datos,columns=['Name','value'])
    Resultado.index=Resultado.index[:]+1
    print("ID de sensor: {:#0X}".format(i.key))
    print(Resultado)
    if data:
        sent = sock.sendto(data, address)
        print('sent {} bytes back to {}'.format(
            sent, address))
