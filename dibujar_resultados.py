import socket
import pickle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np
server =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('localhost',49000))
HEADER=64
FORMAT='utf-8'
Datos_dibujo=[]
def long(i):
    msg_length=int(server.recvfrom(HEADER)[0].decode(FORMAT))
    msg=server.recvfrom(msg_length)[0]
    coeff=pickle.loads(msg)
    Datos_dibujo.append([time.time()]+coeff)
    if coeff[-1]:color='r'
    else:color='g'
    ax[0].plot([Datos_dibujo[-1][0]],coeff[0],color+'o')
    ax[1].plot([Datos_dibujo[-1][0]],coeff[1],color+'o')
    
    #for j in range(2):ax[j].plot(np.array(Datos_dibujo)[:,0],Datos_dibujo[:,j+1],'go')
    
fig, ax=plt.subplots(nrows=2)
anim=animation.FuncAnimation(fig,long,interval=1)
plt.show()
    
