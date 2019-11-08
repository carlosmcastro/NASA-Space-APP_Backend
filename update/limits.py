#encoding: utf-8
#!/usr/bin/env python
import pandas as pd
import numpy as np
import sympy as sp

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
g=6.674*10**-11		#Gravitational constant
au=149597870700

#Determine the coherent intervals of mass and radius for planets and stars.
#NOTE: The data of stars with radii higher than the currently established upper elevation correspond to 0.01% of the total data.
#I prefer to estimate the data on the basis of known densities (although they are few, they cover most cases). 
#And when the database is updated, this limit will be moved by the calculations.
def interval(mass=None): #mass: star mass
	
	if mass:
		plmmaxb=min(plmmax, qmass*mass)
		racomp=[((plmmin*jupmass)/pldmax)*(3/4)*(1/np.pi), ((plmmaxb*jupmass)/pldmin)*(3/4)*(1/np.pi)]
		radlim=np.cbrt(racomp)/earthrad
		radlim.sort()
		return {'m': (plmmin,plmmaxb), 'r': tuple(radlim)}
	else:
		racomp=[((stmmin*sunmass)/stdmax)*(3/4)*(1/np.pi), ((stmmax*sunmass)/stdmin)*(3/4)*(1/np.pi)]
		radlim=np.cbrt(racomp)/sunrad
		radlim.sort()
		return {'m': (stmmin,stmmax), 'r': tuple(radlim)}

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
		return ((mass*sunmass)/((4/3)*np.pi*pow(sunrad*rad, 3)))/1000
	if id==1:
		return ((mass*jupmass)/((4/3)*np.pi*pow(earthrad*rad, 3)))/1000
		
		
#habitable zone qualifier (guarantees the possibility of liquid water, if there is water on the planet)
#teff: Effective temperature, lum: stellar luminance
#lum comes from log(solar) units
def chz(teff, lum):
	lsun=3.83*10**26 #Luminosidad solar. En Watts
	lumi=np.exp(lum)*lsun
	ts=5777 #Kelvin
	ai=27619*10**-5
	bi=38095*10**-9
	ao=1.3786*10**-4
	bo=1.4286*10**-9
	ris=0.72
	ros=1.77
	liminferior=(ris-ai*(teff-ts)-bi*(teff-ts)**2)*np.sqrt(lumi)
	limsuperior=(ros-ao*(teff-ts)-bo*(teff-ts)**2)*np.sqrt(lumi)
	zone=[liminferior, limsuperior]
	return zone #Units UA 

#Auxiliary function to calculate the luminosity, in case the data is missing in the dataset.
#https://exoplanetarchive.ipac.caltech.edu/docs/poet_calculations.html
#As the data proceed in solar radius, that data is obvited.
#resll: stellar radio. On solar radios.
def lumen(teff, resll):
	lsun=3.83*(10**26) #Solar luminosity.
	ts=5777 #Kelvin
	return np.log(lsun*(pow(resll, 2)*pow(teff/ts, 4)))/lsun		
	

#Main collision module. Returns False if they do not collide, returns True if they do.
#sintax: collision((periastro_p1, velocity_p1, star_mass, planet_mass_p1),(periastro_p2, velocity_p2, star_mass, planet_mass_p2))
#p1: Planet 1, p2: Planet 2, discc is optional, it is the "impact range".
def collision(pltone, plttwo, discc=np.pi/180):
	
	rp=np.array([pltone[0], plttwo[0]])*au #periastro
	vl=np.array([pltone[1], plttwo[1]]) #velocity: m/s**2
	mstr=np.array([pltone[2], plttwo[2]])*sunmass #star mass in kilograms
	mplt=np.array([pltone[3], plttwo[3]])*jupmass #planet mass in kilograms
	momang=rp*vl*mplt	#angular moment
	d=(momang**2)/(g*mstr*mplt**2)	
	ex=(d/rp)-1	#excentricidad
	ra=d/(1-ex) #apoastro

	assert ex>=0, "Negative invalid data."
	
	if ex==1:
		return ["Parabolic orbit. Remember, the answer is about collisions in elliptical orbits."]
	if ex>1:
		return ["Hyperbolic orbit. Remember, the answer is about collisions in elliptical orbits."]
	
	a=(rp+ra)/2 #semi-axis major
	b=a*np.sqrt(1-ex**2) #semi-axis-minor
	c=a-rp	#Focus distance
	
	#Orbit ellipses
	e1=sp.Ellipse(sp.Point(-c[0], 0), a[0], b[0])
	e2=sp.Ellipse(sp.Point(-c[1], 0), a[1], b[1])
	
	if e1==e2: #If they're in the same orbit.
		return True
			
	fi=np.array([])
	if e1.intersection(e2):
		fi=np.append(fi, [angut(i.evalf()[0],i.evalf()[1]) for i in e1.intersection(e2)])
		
		timell=[kepeq(mstr, a, ex, u) for u in fi]
		if (timell[:,1]==timell[:,0]).any():	#If they are at the same time at the same angle, of a point of intersection.
			return True
		
		#If they're within each other's time range.
		timellbe=[kepeq(mstr, a, ex, u-discc) for u in fi]
		timellaf=[kepeq(mstr, a, ex, u+discc) for u in fi]
		if (timellbe[:,0]<timell[:,1]).any() and (timell[:,1]<timellaf[:,0]).any():
			return True
		if (timellbe[:,1]<timell[:,0]).any() and (timell[:,0]<timellaf[:,1]).any():
			return True
		
		#Same as before, but scaling, in case the orbits differ too much in their periods.
		scall=np.round(timell.max(axis=1)/timell.min(axis=1))
		if (timellbe[:,0]<timell[:,1]*scall).any() and (timell[:,1]*scall<timellaf[:,0]).any():
			return True
		if (timellbe[:,1]<timell[:,0]*scall).any() and (timell[:,0]*scall<timellaf[:,1]).any():
			return True
		
	else:
		return False
		
def angut(a, b):  #x,y to angule.

	if a>0 and b>0: #First quadrant
		return np.arctan(b/a)
	if a<0 and b>0:	#Second quadrant
		return np.pi-np.arctan(b/a*-1)
	if a<0 and b<0:	#Thirst quadrant
		return np.pi+np.arctan(b/a)
	if a>0 and b<0:	#Four quadrant
		return 2*np.pi+np.arctan(b/a)

#Kepler equation.
def kepeq(mst, aa, exx, th): #star mass, semi-major axis, excentricity, angule 

	c_E=(exx+np.cos(th))/(1+exx*np.cos(th))
	s_E=np.sqrt(1-exx**2)*np.sin(th)/(1+exx*np.cos(th))
	E=np.arctan2(s_E,c_E)
	while E<0:
		E=2*pi+E
	t=(E-exx*s_E)*aa**(3/2)/np.sqrt(g*mst);
	
	return t #time in second