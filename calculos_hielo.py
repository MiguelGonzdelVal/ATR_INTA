class calculos(object):
        
	def __init__(self,fbg_referencia,fbg_deteccion):
		"""Configurates the main parmeters and libraries  

		Args:
			fbg_referencia (int): Reference grating
			fbg_deteccion (int): Detection grating
		"""                
		import logging
		from datetime import datetime
		import numpy 

		#opens a log file only for the current day
		ahora = datetime.now().strftime("%Y_%m_%d")
		self.logging=logging

		self.logging.basicConfig(filename=f'log//{ahora}.log', format='%(asctime)s %(message)s',datefmt='%Y/%m/%d %I:%M:%S %p',level=logging.INFO)
		#convective heat transfer coefficient
		self.h_0 = 2000 #J/(K m)
		#Ice specific heat
		self.cp_i = 2093 #J/(K m)

		self.fbg_referencia=fbg_referencia
		self.fbg_deteccion=fbg_deteccion

		
		from pywt import wavedec
		from scipy.signal import find_peaks
		self.np = numpy
		self.wavedec = wavedec
		self.find_peaks = find_peaks
		self.Hielo=False
		self.Hielo_anterior=False

	def latent_heat(self,T):
		return 4180*(79.7+0.485*T-2.5e-3*T**2)
	
	def specific_heat_water(self,T):
		return 4180*(1+8.29e-5*T**2)
	
	def LWC(self,T,T_rec,V):
		lwc=self.IAR(T,T_rec,V)*917/V/60
		return lwc/0.9
	
	def air_conductivity(self,T_rec):
		T_rec=T_rec+273.15
		return (-12.69 + 2.029*T_rec**0.5)*4.18/3600 #W m−1 K−1
	
	def dynamic_viscosity(self,T_rec):
		T_rec=T_rec+273.15 #K
		return 1e-5/(.12764+124.38/T_rec) #kg/(m s)
	
	def convective_heat_transfer(self,V,T_rec):
		rho_a = 1.225 #kg/m3
		D=0.25*3.16/100 #datos del NACA
		mu_a =self.dynamic_viscosity(T_rec) 
		k_a = self.air_conductivity(T_rec)
		Re=rho_a*V*D/mu_a 
		Pr=0.72
		return 1.14*Re**0.5*Pr**0.4*k_a/D #W/(m K)
	
	def IAR(self,T,T_rec,V):
		rho_ice=917 #kg/m3
		cp_i =self.cp_i
		self.h_0=self.convective_heat_transfer(V,T_rec)
		print(self.h_0)
		L_f=self.latent_heat(T)
		cp_w=self.specific_heat_water(T)
		T_inf = T_rec-V**2/(2*1004)
		iar = -self.h_0*(T-T_rec)/(cp_i*T+V**2/2-L_f+T_inf*cp_w)/rho_ice
		iar_mm_min=iar*1000*60
		return iar_mm_min
		
	def definir_umbrales(self,threshold,nothreshold,V):
		"""Defines the detection thresholds

		Args:
			threshold (float): Detection threshold
			nothreshold (float): Detection of No ice threshold
			V (float): IAS (m/s)
		"""		
		self.threshold=threshold
		self.nothreshold=nothreshold
		self.V=V

	def analisis_hielo(self,Temperatura_procesada,Hielo):
		"""
			Analyzes the signal and returns the icing cloud parameters and if there is or not ice
		Args:
			Temperatura_procesada (float): that will be processed
			Hielo (bool): Ice presence or not (True Ice; False No Ice)

		Returns:
			(Hielo,LWC,IAR,times) (tuple):
				Hielo (bool): Ice presence or not (True Ice; False No Ice)
				LWC (float): Lquid Water Content (g/m3)
				IAR (float): Ice Accretion Rate (mm/min)
				times (list): Times when the ice accretion began

		"""		
		np = self.np
		V=self.V
		LWC = 0
		IAR =0
		texto = f'V={V}\n'
		texto+=f'h={self.convective_heat_transfer(V,0)}\n'
		texto+=f'mu={self.dynamic_viscosity(0)}\n'
		texto+=f'ka={self.air_conductivity(0)}\n'
		print(texto)
		#Coge todo el array de temperaturas y de el coge la diferencia entre el sensor de deteccion y el de referencia.
		Delta_T=np.array(Temperatura_procesada)[:,self.fbg_deteccion]-np.array(Temperatura_procesada)[:,self.fbg_referencia]
        #logica: si hay hielo el algoritmo de deteccion de no hielo debe ser menos exigente (nivel 6)
		if not Hielo:level =7
		else:level = 7
		#Calculates the discrete wavelet transform of the signals
		coeff= self.wavedec(Delta_T, 'db1',level=level)
		#coge como tiempo inicial el primero del array
		t_0=np.array(Temperatura_procesada)[0,0]

        #hace un equiespaciado de tiempos en función de la longitud de la ondicula de mayor nivel (hay otra forma mas elegante de resolver el problema) (ver paper)
		tiempos=np.linspace(np.array(Temperatura_procesada)[0,0]-t_0,np.array(Temperatura_procesada)[-1,0]-t_0,len(coeff[1]))
        
		self.threshold=0.3
		self.nothreshold=0.2

		#Calcula los picos en el rango descrito
		picos, alturas = self.find_peaks(-coeff[1]/2**(level/2),height=self.threshold)
		#calcula los picos negativos (no hielo)
		picos_no, alturas_no = self.find_peaks(coeff[1]/2**(level/2),height=self.nothreshold)
		print(picos,len(coeff[1]))
		
		
		if len(picos)>0:
			if len(picos_no)>0:
				if tiempos[picos_no][-1]>tiempos[picos][-1]:
					Hielo = False
					
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

	def loggear(self,Hielo,IAR):
		"""Saves the icing events in an external file

		Args:
			Hielo (bool): Ice presence or not (True Ice; False No Ice)
			IAR (float): ice accretion rate (mm/min)
		"""		
		
		if Hielo:self.logging.info(f'Hielo={Hielo},{IAR:.2f}mm/min,LWC={IAR*917/70/60:.2f}g/m3')
		else:
			if self.Hielo_anterior:
				self.logging.info(f'Hielo={Hielo}')
			
		self.Hielo_anterior = Hielo
