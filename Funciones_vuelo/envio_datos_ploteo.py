
class COM_Dibujo(object):
    def __init__(self):
        import socket
        import pickle
        self.pickle=pickle
        self.client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ADDR=('localhost',49000)
        
        
    def envio_datos_ploteo(self,coeff,Hielo):
        '''envia datos a un servidor UDP para luego ser ploteados. Es una funcion muy sencilla ya que se los envia masticaditos.
        solo le envia el ultimo dato de cada variable) Le envia coeff.'''
        
        FORMAT='utf-8'
        HEADER = 64
        message=self.pickle.dumps([coeff[0][-1],coeff[1][-1],Hielo])
        msg_length= len(message)
        send_length= str(msg_length).encode(FORMAT)
        send_length+=b' '*(HEADER-len(send_length))
        self.client.sendto(send_length,self.ADDR)
        self.client.sendto(message,self.ADDR)
        
        
        
        
    
    
    

    
    
