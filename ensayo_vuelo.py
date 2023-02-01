from calculos_hielo import calculos
import queue
from Funciones_vuelo.guardado import Guardado_temperaturas
import threading
import pywt
from Umbrales import umbral
import hyperion
import threading
import pandas as pd
from conexion_hyperion import conection
from scipy.signal import find_peaks, peak_prominences
from datetime import datetime
import time
import os
import matplotlib.pyplot as plt
import numpy as np
from client import envio_datos
import servidor_avion
from Funciones_vuelo.envio_datos_ploteo import COM_Dibujo
#Se adquieren los datos del avión:
Hilo_datos_avion=threading.Thread(target=servidor_avion.adquisicion_param_avion).start()

#Parametros
fbg_referencia = 8
fbg_deteccion=2
t_muestreo =0.1

#Comunicacion_dibujo
COM_dib=COM_Dibujo()
#COM_dib.envio_datos_ploteo([[0],[1]])

nombre_archivo=f'Resultados//{int(time.time())}.txt'
n=0
#velocidad por defecto
V=69
#umbral sin hielo
threshold_no_ice =-0.6
#se conecta el programa con interrogador optico
h1=conection()
#Objeto para calculos
Calculo= calculos(fbg_referencia,fbg_deteccion)
#archivo con las calibraciones del perfil de vuelo
perfil = 'Calibraciones//P_vuelo_1.txt'	
h1.calibracion = pd.read_csv(perfil,sep=';')
h1.calibracion.index = h1.calibracion.nombre_fibra
#Crea el archivo de guardado
file=open(nombre_archivo,'w')
file.close()
print(h1.ask_tem(h1,1))
Temperatura=queue.Queue(maxsize=30)	
Temperatura_procesada=[]
Muestras_guardado=300
n_canales = set(h1.calibracion.canal)
Hielo = False
texto=''
while True:
	tiempo_iter=time.time()
	Temperatura.put(h1.ask_tem(h1,1))
	if Temperatura.full():
		while not Temperatura.empty():Temperatura_procesada.append(Temperatura.get())
		threshold = umbral(Temperatura_procesada[-1][-1],V)
		noThreshold=threshold
		Calculo.definir_umbrales(threshold,noThreshold,V)
		if len(Temperatura_procesada)>Muestras_guardado:
                        #recomendable hacerlo en formato de Thread (pierde mucho tiempo)
			Temperatura_procesada=Guardado_temperaturas(Temperatura_procesada,nombre_archivo)
		try:
			(Hielo,LWC,IAR,tiempos_detectados) = Calculo.analisis_hielo(Temperatura_procesada,Hielo)
			COM_dib.envio_datos_ploteo(Calculo.coeff,Calculo.Hielo)
			print(f'velocidad',V,IAR*917/70/60)
			if Hielo:
				texto+=f'{time.time()},Ice t={tiempos_detectados}\nLWC={LWC:.2f}g/m3\nLWC={IAR:.1f}mm/min'
				#print(f'Ice t={tiempos_detectados}\nLWC={LWC:.2f}g/m3\nLWC={IAR:.1f}mm/min')
			else:
				texto+=f'{time.time()},No hielo'
				#print('No hielo')
			envio_datos(float(Hielo),float(LWC),float(IAR))
			n+=1
			if n==10:
				n=0
				texto=''
		except Exception as e:print(e)
		
	if t_muestreo-time.time()+tiempo_iter>0:time.sleep(t_muestreo-time.time()+tiempo_iter)

	
	

