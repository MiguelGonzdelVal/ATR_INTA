#%%IMPORTACIONES
from calculos_hielo import calculos
import queue
import threading
from Umbrales import umbral

import threading
import pandas as pd
from conexion_hyperion import conection
import time
from client import envio_datos
import servidor_avion
from Funciones_vuelo.envio_datos_ploteo import COM_Dibujo
from Funciones_vuelo.guardado import Guardado_temperaturas
import logging
#%%Se adquieren los datos del avión:
AVION=servidor_avion.ATR_data()
Hilo_datos_avion=threading.Thread(target=AVION.adquisicion_param_avion).start()

#%%Parametros
fbg_referencia = 8
fbg_deteccion=2
t_muestreo =0.1
#velocidad por defecto
V=69
#umbral sin hielo
threshold_no_ice =-0.6

#%%Comunicacion_dibujo
COM_dib=COM_Dibujo()
borrado = False
#%%Se abre un hilo para guardado de datos:


n=0

#se conecta el programa con interrogador optico
h1=conection()
#Objeto para calculos
Calculo= calculos(fbg_referencia,fbg_deteccion)
#archivo con las calibraciones del perfil de vuelo
perfil = 'Calibraciones//P_vuelo_1.txt'	
h1.calibracion = pd.read_csv(perfil,sep=';')
h1.calibracion.index = h1.calibracion.nombre_fibra
#Crea el archivo de guardado

print(h1.ask_tem(h1,1))

Temperatura=queue.Queue(maxsize=30)	
Temperatura_procesada=[]

#%% Se abre el hilo de guardado de datos
muestras_guardado=3600
Hilo_guardado=threading.Thread(target=Guardado_temperaturas,args=(muestras_guardado,)).start()

n_canales = set(h1.calibracion.canal)
Hielo = False
texto=''
Hielo_anterior=False

while True:
	tiempo_iter=time.time()
	Temperatura.put(h1.ask_tem(h1,1))
	if Temperatura.full():
		while not Temperatura.empty():
			Temperatura_procesada.append(Temperatura.get())
		threshold = umbral(Temperatura_procesada[-1][-1],V)
		noThreshold=threshold
		Calculo.definir_umbrales(threshold,noThreshold,V)
		#esto hay que limpiarlo del __main__
		if borrado:
			Temperatura_procesada=Temperatura_procesada[muestras_guardado//2:]
			borrado = False
		try:
			(Hielo,LWC,IAR,tiempos_detectados) = Calculo.analisis_hielo(Temperatura_procesada,Hielo)
			COM_dib.envio_datos_ploteo(Calculo.coeff,Calculo.Hielo)
			Calculo.loggear(Hielo,IAR)
			envio_datos(float(Hielo),float(LWC),float(IAR))

		except Exception as e:
			Calculo.logging.error(e)
	if t_muestreo-time.time()+tiempo_iter>0:time.sleep(t_muestreo-time.time()+tiempo_iter)

	
	

