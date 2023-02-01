


def conection():
	import hyperion
	channel = 1
	conexion_terminada = False
	mensaje_conexion = True
	def ask_tem(h1,channel):
		import time
		out =[time.time()]
		i=1
		for wl in h1.peaks[channel]:
			A=h1.calibracion['A'].loc[f'FBG{i}']
			B=h1.calibracion['B'].loc[f'FBG{i}']
			C=h1.calibracion['C'].loc[f'FBG{i}']
			D=h1.calibracion['D'].loc[f'FBG{i}']
			i+=1
			out.append(Temperatura(wl,A,B,C,D))
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
