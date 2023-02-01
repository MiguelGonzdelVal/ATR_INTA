class calculos(object):
        
	def __init__(self,fbg_referencia,fbg_deteccion):
                
                #Aqui esto es un potencial error. He puesto un h_0 cte. Debería ser calculable (mirar mi paper)
		self.h_0 = 2000 #J/(K m)
		
		self.cp_i = 2093 #J/(K m)
		self.fbg_referencia=fbg_referencia
		self.fbg_deteccion=fbg_deteccion
		import numpy 
		from pywt import wavedec
		from os import system
		from scipy.signal import find_peaks, peak_prominences
		self.np = numpy
		self.wavedec = wavedec
		self.find_peaks = find_peaks
		self.system = system
	def latent_heat(self,T):
		return 4180*(79.7+0.485*T-2.5e-3*T**2)
	def specific_heat_water(self,T):
		return 4180*(1+8.29e-5*T**2)
	def LWC(self,T,T_rec,V):
		lwc=self.IAR(T,T_rec,V)*917/V/60
		return lwc/0.9
	def IAR(self,T,T_rec,V):
		rho_ice=917 #kg/m3
		cp_i =self.cp_i
		L_f=self.latent_heat(T)
		cp_w=self.specific_heat_water(T)
		T_inf = T_rec-V**2/(2*1004)
		iar = -self.h_0*(T-T_rec)/(cp_i*T+V**2/2-L_f+T_inf*cp_w)/rho_ice
		iar_mm_min=iar*1000*60
		return iar_mm_min
		
	def definir_umbrales(self,threshold,nothreshold,V):
		self.threshold=threshold
		self.nothreshold=nothreshold
		self.V=V
	def analisis_hielo(self,Temperatura_procesada,Hielo):
		np = self.np
		V=self.V
		LWC = 0
		IAR =0
		#Coge todo el array de temperaturas y de el coge la diferencia entre el sensor de deteccion y el de referencia.
		Delta_T=np.array(Temperatura_procesada)[:,self.fbg_deteccion]-np.array(Temperatura_procesada)[:,self.fbg_referencia]
                #logica: si hay hielo el algoritmo de deteccion de no hielo debe ser menos exigente (nivel 6)
		if not Hielo:level =7
		else:level = 7
		#calcula la transformada ondicular de la temperatura
		coeff= self.wavedec(Delta_T, 'db1',level=level)
		#coge como tiempo inicial el primero del array
		t_0=np.array(Temperatura_procesada)[0,0]
                #hace un equiespaciado de tiempos en función de la longitud de la ondicula de mayor nivel (hay otra forma mas elegante de resolver el problema)
		tiempos=np.linspace(np.array(Temperatura_procesada)[0,0]-t_0,np.array(Temperatura_procesada)[-1,0]-t_0,len(coeff[1]))
                #QUITAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self.threshold=0.3
		self.nothreshold=0.2

		#Calcula los picos en el rango descrito
		picos,alturas = self.find_peaks(-coeff[1]/2**(level/2),height=self.threshold)
		#calcula los picos negativos (no hielo)
		picos_no,alturas_no = self.find_peaks(coeff[1]/2**(level/2),height=self.nothreshold)
		print(picos,len(coeff[1]))
		
		#self.system('cls')
		if len(picos)>0:
			if len(picos_no)>0:
				if tiempos[picos_no][-1]>tiempos[picos][-1]:
					Hielo = False
					print(f'No ice t={tiempos[picos_no]}:.2f')
				else:
					Hielo = True
					LWC=self.LWC(np.array(Temperatura_procesada)[-1,1],np.array(Temperatura_procesada)[-1,-1],V)
					IAR=self.IAR(np.array(Temperatura_procesada)[-1,1],np.array(Temperatura_procesada)[-1,-1],V)

			else:
				Hielo = True
				LWC=self.LWC(np.array(Temperatura_procesada)[-1,0],np.array(Temperatura_procesada)[-1,7],V)
				IAR=self.IAR(np.array(Temperatura_procesada)[-1,1],np.array(Temperatura_procesada)[-1,-1],V)
		else:Hielo = False
		if Temperatura_procesada[-1][-1]-V**2/(2*1004.5) >100: Hielo = False
		#finalmente guarda las variables que serán transmitidas por UDP a un servidor local
		coeff[1]=-coeff[1]/2**(level/2)
		coeff[0]=coeff[0]/2**(level/2)
		self.coeff=coeff
		self.Delta_T=Delta_T
		self.Hielo=Hielo
		return (Hielo,IAR*917/V/60,IAR,tiempos[picos])
