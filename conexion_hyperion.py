


def conection():
	"""La funcion devuelve un objeto hyperion en el que se calculan las temperaturas

	Returns:
		object: Objeto hyperion con una nueva funcion ask_tem que te da las temperaturas
				de los sensores
	"""	
	import hyperion
	import numpy as np
	channel = 1
	conexion_terminada = False
	mensaje_conexion = True
	

	def ask_tem(h1,channel):
		import time
		picos=np.array(h1.peaks[channel])
		out =[time.time()]+[np.nan for _ in h1.calibracion.nombre_sensor]
		
		h1.calibracion.index=h1.calibracion.nombre_sensor
		

		for i,sensor in enumerate(h1.calibracion.index):
			lamb_min=h1.calibracion['lambda_min'].loc[sensor]
			lamb_max=h1.calibracion['lambda_max'].loc[sensor]
			wl=picos[np.where((picos>lamb_min)&(picos<lamb_max))[0]][0]
			A=h1.calibracion['A'].loc[sensor]
			B=h1.calibracion['B'].loc[sensor]
			C=h1.calibracion['C'].loc[sensor]
			D=h1.calibracion['D'].loc[sensor]
			out[i+1]=Temperatura(wl,A,B,C,D)
		return out
	def Temperatura(wavelength,A,B,C,D):
		return A*wavelength**3+B*wavelength**2+C*wavelength+D	
	while not conexion_terminada:
		try:
			h1 = hyperion.Hyperion('10.0.0.55')
			print(len(h1.peaks[channel]))
			h1.Temperatura=Temperatura
			h1.ask_tem=ask_tem
			
			conexion_terminada=True
		except Exception as ex:
			#Si no se conecta a Hyperion no funcionara
			print(ex)
			if mensaje_conexion:
				mensaje_conexion=False
				print('Cuidado no va a funcionar!!!!!!!!!!')
		return h1
