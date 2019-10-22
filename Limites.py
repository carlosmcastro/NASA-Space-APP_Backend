#encoding: utf-8
#!/usr/bin/env python
import pandas as pd
import math
import numpy as np

#Base de datos.
data=pd.read_csv('total_data.csv')

#Se han limpiado los datos de sistemas estelares binarios.
data=data.drop(data.loc[a['pl_cbflag']==1].index)

#Masa minima de planeta (masas de jupiter).
plmmin=min([i for i in data.pl_bmassj if not str(i)=='nan'])
#Masa maxima de planeta (masas de jupiter).
plmmax=max([i for i in data.pl_bmassj if not str(i)=='nan'])

#Masa minima de estrella (masas solares).
stmmin=min([i for i in data.st_mass if not str(i)=='nan'])
#Masa maxima de estrella (masas solares).
stmmax=max([i for i in data.st_mass if not str(i)=='nan'])

#Calculo de qmass, cociente maximo de masa, entre estrella y planeta.
qmass=0
for i in list(set(data.pl_hostname)):
	stmassaux=list(data.loc[data['pl_hostname']==i].st_mass)[0]
	plmassaux=list(data.loc[data['pl_hostname']==i].pl_bmassj)
	for u in plmassaux:
		if qmass<(u/stmassaux):
			qmass=u/stmassaux #Esta no es una ecuación de cambio, las unidades de las dos masas son distintas, pero la proporción sirve como comparación estadistica.
			
#Densidad minima del planeta (kg / m ** 3)
pldmin=min([i for i in data.pl_dens if not str(i)=='nan'])*1000
#Densidad maxima del planeta (kg / m ** 3).
pldmax=max([i for i in data.pl_dens if not str(i)=='nan'])*1000


#Densidad minima de la estrella (kg / m ** 3).
stdmin=min([i for i in data.st_dens if not str(i)=='nan'])*1000
#Densidad maxima de la estrella (kg/ m ** 3).
stdmax=max([i for i in data.st_dens if not str(i)=='nan'])*1000


#Id==1 para planetas 
#Id==0 para estrellas
#rad: radio en radios terrestres o solares
#mass: (masa_estelar) o (masa_estelar, masa_planetaria)
#Devuelve una tupla booleana, el primer valor valida el radio y la meda.
def central(id, rad, *mass):
	valid=[]
	if id==1:
		if (plmmin<=mass[1]<=plmmax) and ((mass[1]/mass[0])<=qmass):
			valid.append(True)
		jupmass=mass[1]*1.898*10**27 #masa jupiter kg
		#Radio minimo del planeta radio m**3
		plramin=(((mass[1]*jupmass)/pldmin)*(4/3)*(1/math.pi)
		#Radio maximo del planeta radio m**3
		plramax=((mass[1]*jupmass)/pldmax)*(4/3)*(1/math.pi)
		terrad=rad*6371*(10**3) #Radio terrestre en metros.
		if (plramin<=pow(terrad,3)<=plramax):
			valid.append(True)
		valid.reverse()
		return valid
	if id==0:
		if stmmin<mass[0]<stmmax:
			valid.append(True)
		sunmass=mass[0]*1.989*10**30 #masa solar kg
		#Radio minimo de la estrella al cubo m**3
		stramin=(((mass[0]*sunmass)/stdmin)*(4/3)*(1/math.pi)
		#Radio maximo de la estrella al cubo m**3
		stramax=(((mass[0]*sunmass)/stdmax)*(4/3)*(1/math.pi)
		sunrad=rad*695510 *(10**3) #Radio solar en metros.
		if (stramin<=pow(terrad,3)<=stramax):
			valid.append(True)
		valid.reverse()
		return valid

#Calificador de zona habitabitable (garantiza la posibilidad de agua liquida)
#teff Temperatura efectiva, lum luminosidad estelar
def chz(teff, lum):
	ts=5700 #Kelvin
	ai=27619*(10**-5)
	bi=38095*(10**-9)
	ao=1,3786*(10**-4)
	bo=1,4286*(10**-9)
	ris=0,72
	ros=1,77
	zone=[ris-(ai*(teff-ts))-(bi*((teff-ts)**2))*math.sqrt(lum),ros-(ao*(teff-ts))-(bo*((teff-ts)**2))*math.sqrt(lum)]
	return zone








	
#0 aposatro
#1 excentricidad
#2 masa planeta
#3 precision
#Diagrama una orbita en base a una precisión, para ser analizada posteriormente.
def orb(*arg):
	gg=6674*(10**-11) #Constante gravitatoria
	a=arg[0]/(1+arg[1]) #semieje mayor, elipse
	b=a*(math.sqrt(1/(1-pow(arg[1],2)))) #semieje menor
	tt=math.sqrt((4*(math.pi**2)*(a**3))/(gg*arg[2])) 
	c=arg[1]*a
	
	ang=0
	dang=(2*math.pi)/arg[3]
	locate={}
	for i in range(arg[3]):
		x=-c+math.cos(dang)/math.sqrt((cos(dang)/a)**2)+((sen(dang)/b)**2)) #centrado en un foco estelar
		y=math.sen(dang)/math.sqrt((cos(dang)/a)**2)+((sen(dang)/b)**2))
		locate[i]=(x,y)
	return locate

#Herramienta para procesar los datos de orbitas.
def rotras(*arg):
	#equivalente de matriz rotacional. Y traslación.
	x=math.cos(arg[0])*arg[1]-math.sin(arg[0])*arg[2] + arg[3]
	y=math.sen(arg[0])*arg[1]+math.cos(arg[0])*arg[2] + arg[4]
	return [x, y]
	
#Ejecutando varias veces esta función, se pueden saber los cruces de las orbitas.
def cruces(prec, *kargs):
	interseca=[]
	for i in range(prec/2):
		for u in range(prec):
			if (kargs[0][i][0]<=kargs[1][u][0]<=kargs[0][prec-i][0]) and (kargs[0][i][1]<=kargs[1][u][1]<=kargs[0][prec-i][1]):
					interseca.append((kargs[1][u][0],kargs[1][u][1]))
	return interseca

#Pseudo-codigo para calculo de orbita eliptica en funcion del tiempo.
#Sin modificaciones de unidades añadidas.
#period: periodo
#a: semieje mayor, apo: apoastro, peri: periastro, gg: G, mass: masa, locatedd: simulación de elipse en tuplas x,y.
#acc, pseudo aceleración, tem, interpolacion del periodo, temv, interpolación de la velocidad, basado en los extremos.
#
def tempo(period, a, apo, peri, gg, mass, locatedd):
	vi=math.sqrt((gg*mass)*((2/apo)-(1/a)))
	vf=math.sqrt((gg*mass)*((2/pero)-(1/a)))
	acc=(vf-vi)/(periodo/2)
	tem=np.linspace(0, period/2, int(len(locatedd)/2))
	temv=np.linspace(vi, vf, (int(len(locatedd)/2)))
	return [vi, vf, acc, tem, temv]
	
	
	
	
	
	
	
	
	
	




