#encoding: utf-8
#!/usr/bin/env python
import pandas as pd
import math
import numpy as np

#Database.
data=pd.read_csv('total_data.csv')

#Binary stellar system data has been cleansed.
data=data.drop(data.loc[data['pl_cbflag']==1].index)

#Null values are filtered out.

#Minimum mass of planet (masses of jupiter).
plmmin=min(data[data.pl_bmassj.isnull()==False].pl_bmassj)
#Maximum mass of planet (masses of jupiter).
plmmax=max(data[data.pl_bmassj.isnull()==False].pl_bmassj)

#Minimal mass of star (solar masses).
stmmin=min(data[data.st_mass.isnull()==False].st_mass)
#Maximum star mass (solar masses).
stmmax=max(data[data.st_mass.isnull()==False].st_mass)

#Calculation of qmass, maximum mass quotient, between planet and star.
qmass=0
for i in list(set(data.pl_hostname)):
	stmassaux=list(data.loc[data['pl_hostname']==i].st_mass)[0]
	plmassaux=list(data.loc[data['pl_hostname']==i].pl_bmassj)
	for u in plmassaux:
		if qmass<(u/stmassaux):
			qmass=u/stmassaux #This is not an equation of change, the units of the two masses are different, but the ratio functions as a statistical comparison.

#Minimum density of the planet (kg / m ** 3)
pldmin=min(data[data.pl_dens.isnull()==False].pl_dens)*1000
#Maximum density of the planet (kg / m ** 3).
pldmax=max(data[data.pl_dens.isnull()==False].pl_dens)*1000
		
#Minimum density of the star (kg / m ** 3).
stdmin=min(data[data.st_dens.isnull()==False].st_dens)*1000
#Maximum density of the star (kg/ m ** 3).
stdmax=max(data[data.st_dens.isnull()==False].st_dens)*1000

#Units Constants
sunmass=1.989*10**30 #Solar mass in kg
sunrad=695510 *(10**3) #Solar radius in metros.
jupmass=1.898*(10**27) #Jupiter mass in kg
earthrad=6371*(10**3) #Earth radius in meters.

#Determine the coherent intervals of mass and radius for planets and stars.
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
#mass, in jupiter masses or solar masses, radius in solar radius, or earth radius		
def dens(id, mass, rad): #Density in gr/cm**3
	if id==0:
		return ((mass*sunmass)/((4/3)*math.pi*pow(sunrad*rad, 3)))/1000
	if id==1:
		return ((mass*jupmass)/((4/3)*math.pi*pow(earthrad*rad, 3)))/1000
		
		
#habitable zone qualifier (guarantees the possibility of liquid water, if there is water on the planet)
#teff: Effective temperature, lum: stellar luminance
#lum comes from log(solar) units
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

#Auxiliary function to calculate the luminosity, in case the data is missing in the dataset.
#https://exoplanetarchive.ipac.caltech.edu/docs/poet_calculations.html
#As the data proceed in solar radius, that data is obvited.
#resll: stellar radio. On solar radios.
def lumen(teff, resll):
	lsun=3.83*(10**26) #Solar luminosity.
	ts=5777 #Kelvin
	return math.log(lsun*(pow(resll, 2)*pow(teff/ts, 4)))/lsun		
		
		
		
		
		
		
		
		
		
		
		
		
