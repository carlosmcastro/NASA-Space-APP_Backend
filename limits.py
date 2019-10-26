#encoding: utf-8
#!/usr/bin/env python
import pandas as pd
import math
import numpy as np


#Base de datos.
data=pd.read_csv('total_data.csv')

#Se han limpiado los datos de sistemas estelares binarios.
data=data.drop(data.loc[data['pl_cbflag']==1].index)

#Se filtran valores nulos.

#Masa minima de planeta (masas de jupiter).
plmmin=min(data[data.pl_bmassj.isnull()==False].pl_bmassj)
#Masa maxima de planeta (masas de jupiter).
plmmax=max(data[data.pl_bmassj.isnull()==False].pl_bmassj)

#Masa minima de estrella (masas solares).
stmmin=min(data[data.st_mass.isnull()==False].st_mass)
#Masa maxima de estrella (masas solares).
stmmax=max(data[data.st_mass.isnull()==False].st_mass)

#Calculo de qmass, cociente maximo de masa, entre estrella y planeta.
qmass=0
for i in list(set(data.pl_hostname)):
	stmassaux=list(data.loc[data['pl_hostname']==i].st_mass)[0]
	plmassaux=list(data.loc[data['pl_hostname']==i].pl_bmassj)
	for u in plmassaux:
		if qmass<(u/stmassaux):
			qmass=u/stmassaux #Esta no es una ecuación de cambio, las unidades de las dos masas son distintas, pero la proporción sirve como comparación estadistica.

#Densidad minima del planeta (kg / m ** 3)
pldmin=min(data[data.pl_dens.isnull()==False].pl_dens)*1000
#Densidad maxima del planeta (kg / m ** 3).
pldmax=max(data[data.pl_dens.isnull()==False].pl_dens)*1000
		
#Densidad minima de la estrella (kg / m ** 3).
stdmin=min(data[data.st_dens.isnull()==False].st_dens)*1000
#Densidad maxima de la estrella (kg/ m ** 3).
stdmax=max(data[data.st_dens.isnull()==False].st_dens)*1000

#Units Constants
sunmass=mass[0]*1.989*10**30 #masa solar kg
sunrad=rad*695510 *(10**3) #Radio solar en metros.
jupmass=1.898*(10**27) #masa jupiter kg
earthrad=6371*(10**3) #Radio terrestre en metros.

#Determina los intervalos coherentes de masa y radio, para planetas y estrellas.
def interval(mass=None): #mass: star mass
	
	if mass:
		plmmaxb=min(plmmax, qmass*mass)
		racomp=[((plmmin*jupmass)/pldmin)*(3/4)*(1/math.pi), ((plmmaxb*jupmass)/pldmax)*(3/4)*(1/math.pi)]
		radlim=np.cbrt(racomp)/earthrad
		return {'m': (plmmin,plmmaxb), 'r': tuple(radlim.sort())}
	else:
		racomp=[((stmmin*sunmass)/stdmin)*(3/4)*(1/math.pi), ((stmmax*sunmass)/stdmax)*(3/4)*(1/math.pi)]
		radlim=np.cbrt(racomp)/sunrad
		return {'m': (stmmin,stmmax), 'r': tuple(radlim.sort())}

#id=0 Star, id=1 Planet	
#test(0,m=massstar, r=starrad)	
#test(1,m=(massstar, massplanet), r=planetrad)	
def test(id, **kward):
	
	if id==1:
		
		tt={}
		tested=interval(kward['m'][0])
		
		if tested['m'][0]<=kward['m'][1]<=tested['m'][1]:
			tt['m']=True
		else:
			tt['m']=False
			
		if tested['r'][0]<=kward['r']<=tested['r'][1]:
			tt['r']=True
		else:
			tt['r']=False

		return tt
		
	if id==0:
	
		tt={}
		tested=interval()
		
		if tested['m'][0]<=kward['m']<=tested['m'][1]:
			tt['m']=True
		else:
			tt['m']=False
			
		if tested['r'][0]<=kward['r']<=tested['r'][1]:
			tt['r']=True
		else:
			tt['r']=False

		return tt		

#id=0 Star, id=1 Planet
#masa, en masas de jupiter ó masas solares, radios en radios solares, o radios terrestres		
def dens(id, mass, rad): #Densidad en gr/cm**3
	if id==0:
		return ((mass*sunmass)/((4/3)*math.pi*pow(sunrad*rad, 3)))/1000
	if id==1:
		return ((mass*jupmass)/((4/3)*math.pi*pow(earthrad*rad, 3)))/1000
		
		
#Calificador de zona habitabitable (garantiza la posibilidad de agua liquida)
#teff Temperatura efectiva, lum luminosidad estelar
#lum procede de unidades log(solar)
def chz(teff, lum):
	lsun=3.83*(10**26) #Luminosidad solar. En Watts
	lumi=exp(lum)*lsun
	ts=5777 #Kelvin
	ai=27619*(10**-5)
	bi=38095*(10**-9)
	ao=1,3786*(10**-4)
	bo=1,4286*(10**-9)
	ris=0,72
	ros=1,77
	zone=[ris-(ai*(teff-ts))-(bi*((teff-ts)**2))*math.sqrt(lumi),ros-(ao*(teff-ts))-(bo*((teff-ts)**2))*math.sqrt(lumi)]
	return zone

#Función auxiliar para calcular la luminosidad, en casa de que el dato falte en el dataset.
#https://exoplanetarchive.ipac.caltech.edu/docs/poet_calculations.html
#Como los datos proceden en radios solares, se obvia ese dato.
#resll: radio estelar. En radios solares.
def lumen(teff, resll):
	lsun=3.83*(10**26) #Luminosidad solar.
	ts=5777 #Kelvin
	return math.log(lsun*(pow(resll, 2)*pow(teff/ts, 4)))/lsun		
		
		
		
		
		
		
		
		
		
		
		
		
