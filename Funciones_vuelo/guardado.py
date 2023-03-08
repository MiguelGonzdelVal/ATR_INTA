
def Guardado_temperaturas(muestras_guardado):
	""" Hilo que corre en paralelo al programa __main__. Cuando Temperatura_procesada
		supera un cierto tamaño se guardan los datos en un archivo y posteriormente se borran
		datos. Se corre el riesgo de perder datos por lo que se tiene que llamar directamente del
		main. Se da el segundo a partir del cual se debe borrar para que el __main__lo ejecute.

	Args:
		
		muestras_guardado (_type_): _description_

	
	"""	
	
	from datetime import datetime
	import time
	ahora = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	nombre_archivo=f'Resultados//{ahora}.txt'
	file=open(nombre_archivo,'w')
	file.write('timestamp')
	for i in range(1,9):file.write(f',FBG_{i}')
	file.write('\n')
	file.close()
	
	while True:
		import __main__
		if (len(__main__.Temperatura_procesada)>=muestras_guardado) and not __main__.borrado:
			print('GUARDANDO DATOS...')
			file=open(nombre_archivo,'a')
			for muestra in __main__.Temperatura_procesada[:muestras_guardado//2]:
				for m in muestra[:-1]:
					file.write(f'{m:.2f},')
				file.write(f'{muestra[-1]:.2f}\n')
			file.close()
			__main__.borrado=True
		else:time.sleep(3)
