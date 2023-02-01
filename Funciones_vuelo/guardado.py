
def Guardado_temperaturas(Temperatura_procesada,nombre_archivo):
	
	file=open(nombre_archivo,'a')
	Muestras_guardado=len(Temperatura_procesada)
	for i in range(Muestras_guardado//2):
		for Temp in Temperatura_procesada[i]:
			if Temp<1e6:file.write(f'{Temp:.2f},')
			else:file.write(f'{Temp},')
		file.write(f'\n')
	#for i in range(Muestras_guardado//2):
	#	del Temperatura_procesada[0]
		
	file.close()
	return Temperatura_procesada
