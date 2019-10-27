#encoding: utf-8
#!/usr/bin/env python
#Information module from alien pet: Bob.

#Example of use: HelpBob.opt('GJ 3021 b', 1, 'pl_pelink') #Link Information [Dict]
#Example of use: HelpBob.quest('whatexo')	#Information "What is Exoplanet?" [Dict]
#Example of use: HelpBob.opt(whopl, st_age=2, mmax=32) #Plantets with stars of 2 Gyr old, and less to 32 (Jupiter mass) [List]
#DO NOT MIX STAR DATA WITH PLANETARY DATA.
import pandas as pd

data=pd.read_csv('total_data.csv')

#Data from binary stellar systems have been cleaned.
data=data.drop(data.loc[data['pl_cbflag']==1].index)

#astro is the name of the star for st_dist, st_age, st_spstr.
#astro is the name of a planet for all other cases.
#num=0 Star, num=1 Planet
def opt(astro, num, *args):
	info={}
	if num==0:
		if 'st_dist' in args:      	#Distance from the system to ours (parsecs)
			info['distancia']=list(data.loc[data['pl_hostname']==astro].st_dist)[0]
		if 'st_age' in args:      	#Star age in Gyrs, billions of years.
			info['age']=[list(data.loc[data['pl_hostname']==astro].st_age)[0], str(list(data.loc[data['pl_hostname']==astro].st_age)[0]/4.6)+' the age of the sun.']	
		if 'st_spstr' in args:				#It gives the star classification.
			tata=''
			morgank=str(list(data.loc[data['pl_hostname']==astro].st_spstr)[0])
			#Letters:
			if 'W' in morgank:
				tata+="Wolf–Rayet "
			if 's' in morgank:
				tata+="Subdwarf star "
			if 'L' in morgank:
				tata+="Brown dwarfs "
			if 'T' in morgank:
				tata+="Cool brown dwarfs  "
			if 'A' in morgank:
				tata+="Bluish-white "
			if 'F' in morgank:
				tata+="Yellow-white "
			if 'O' in morgank:
				tata+="Blue "
			if 'B' in morgank:
				tata+="Blue-white "
			if 'G' in morgank:
				tata+="Yellow "
			if 'K' in morgank:
				tata+="Orange "
			if 'M' in morgank:
				tata+="Red "
			
			#Roman numerals.
			if 'VII' in morgank:
				tata+="white dwarfs "
			elif 'VI' in morgank:
				tata+="sub-dwarfs "
			elif 'IV' in morgank:
				tata+="sub-giants "
			elif 'V' in morgank:
				tata+="Main-Sequence "
			elif 'III' in morgank:
				tata+="regular-giant "
			elif 'II' in morgank:
				tata+="bright-giant "
			elif 'I' in morgank:
				tata+="supergiant "
				
			info['MK']=[morgank,tata] #Star type in notation and in common language.
	
	if num==1:	
		if (int(data.loc[data['pl_name']==astro].pl_kepflag)==1) or (int(data.loc[data['pl_name']==astro].pl_k2flag)==1):
			if ('pl_kepflag' in args) or ('pl_k2flag' in args):	#If it is data from Mission Kepler 1 or K2.
				file=open('HelpBob/Mision_Kepler.txt')
				misi=[file.read(), "https://www.nasa.gov/mission_pages/kepler/main/index.html", "https://es.wikipedia.org/wiki/Kepler_(sat%C3%A9lite)#Segunda_Luz_(K2)"]
				file.close()
				info['kepler']=misi
		if 'pl_facility' in args:	#Name of the installation of observations of discovery of planets.
			info['instalacion']=list(data.loc[data['pl_name']==astro].pl_facility)[0]
		if 'pl_disc' in args:		#Year of Planet Discovery
			info['year']=list(data.loc[data['pl_name']==astro].pl_disc)[0]
		if 'pl_locale' in args:		#Place where the planet was discovered ( ground, space or both)
			info['lugar']=list(data.loc[data['pl_name']==astro].pl_locale)[0]
		if 'pl_telescope' in args:	#Telescope that discovered the planet
			info['telescopio']=list(data.loc[data['pl_name']==astro].pl_telescope)[0]
		if 'pl_instrument' in args:	#Planet Discovery Instrument.
			info['instrument']=list(data.loc[data['pl_name']==astro].pl_instrument)[0]
		if 'pl_mnum' in args:		#Number of moons in the planetary system (zero for now)
			info['lunas']=list(data.loc[data['pl_name']==astro].pl_mnum)[0]
		if 'pl_pnum' in args:		#Numbers of planets in the planetary system.
			info['planet_number']=list(data.loc[data['pl_hostname']==astro].pl_pnum)[0]
		if 'pl_pelink' in args:		#Link to the exoplanet encyclopedias.
			info['links']=['https://exoplanets.nasa.gov/' ,list(data.loc[data['pl_name']==astro].pl_pelink)[0]]
			if 'pl_edelink' in args:		#Link to another website, but there are fewer links available.
				info['links'].append(list(data.loc[data['pl_name']==astro].pl_edelink)[0])
	return info
		
def quest(*ask):
	info={}
	if 'whatexo' in ask: #What is an exoplanet? Definition of parsecs, nearest and farthest exoplanet
		file=open('HelpBob/what_exoplanets.txt')
		near=list(data[data.st_dist==min(data.st_dist)].pl_name)
		farth=list(data[data.st_dist==max(data.st_dist)].pl_name)

		if len(near)<2:
			datn='The nearest exoplanet found is called '+near[0]+" and it's aprox. "+str(min(data.st_dist))+' parsecs away.'
		else:
			datn='The nearest exoplanets found are called '+", ".join(near)+" and they're aprox. "+str(min(data.st_dist))+' parsecs away.'
		if len(farth)<2:
			datf='The farthest exoplanet found is called '+farth[0]+" and it's aprox. "+str(max(data.st_dist))+' parsecs away.'
		else:
			datf='The farthest exoplanets found are called '+", ".join(farth)+" and they're aprox. "+str(max(data.st_dist))+' parsecs away.'
		
		#Calculations made with NASA's Juno spacecraft
		parse="To travel to one parsec distance would take about 3.26 years at the speed of light. Our fastest rocket built would take about 9651 years."

		info['exo_definition']={'title': 'What is an exoplanet?', 'content': file.read()+'\n\n'+datn+'\n'+datf+'\n\n'+parse}
		file.close()
	
	if 'claexo' in ask: #Information about the classification of stars and planets.
		file=open('HelpBob/names_exoplanets.txt')
		info['exo_clasification']={'title': 'Exoplanet naming convention', 'content': file.read()}
		file.close()
	
	if 'teff' in ask: #Effective Temperature of star
		file=open('HelpBob/temp_effective.txt')
		cold=list(set(data[data.st_teff==min(data[data.st_teff.isnull()==False].st_teff)].pl_hostname))
		hot=list(set(data[data.st_teff==max(data[data.st_teff.isnull()==False].st_teff)].pl_hostname))
		
		if len(cold)<2:
			datc='The star with the lowest Effective Temperature found is called '+cold[0]+" and it's aprox. "+str(min(data[data.st_teff.isnull()==False].st_teff))+' Kelvins.'
		else:
			datc='The stars with the lowest Effective Temperature found are called '+", ".join(cold)+" and they're aprox. "+str(min(data[data.st_teff.isnull()==False].st_teff))+' Kelvins.'
		if len(hot)<2:
			dath='The star with the highest Effective Temperature found is called '+hot[0]+" and it's aprox. "+str(max(data[data.st_teff.isnull()==False].st_teff))+' Kelvins.'
		else:
			dath='The stars with the highest Effective Temperature found are called '+", ".join(hot)+" and they're aprox. "+str(max(data[data.st_teff.isnull()==False].st_teff))+' Kelvins.'
			
		kelvi="The Kelvin is one of the most widely used temperature units in physics. Because conveniently its 0 is the absolute zero (there is no object colder than 0 Kelvin).\n\nA cup of hot coffee has about 322 K, the effective temperature of the sun is 5778 k, 18 times the temperature of a coffee. \n\nHowever, with 18 hot cups you could not reach the temperature of the sun, as this is a statistical measure of heat. In addition, the sun in its deepest layers can reach 15 million Kelvin."
		
		info['temp_effectiva']={'title': "What is Effective Temperature?", 'content': file.read()+'\n\n'+datc+'\n'+dath+'\n\n'+kelvi}
		file.close()
	
	if 'teeqt' in ask: #Equilibrium Temperature of a planet. Brief description of the structure of the Earth.
		file=open('HelpBob/temp_eqt.txt')
		cold=list(set(data[data.pl_eqt==min(data[data.pl_eqt.isnull()==False].pl_eqt)].pl_name))
		hot=list(set(data[data.pl_eqt==max(data[data.pl_eqt.isnull()==False].pl_eqt)].pl_name))
		
		if len(cold)<2:
			datc='The planet with the lowest Equilibrium Temperature found is called '+cold[0]+" and it's aprox. "+str(min(data[data.pl_eqt.isnull()==False].pl_eqt))+' Kelvins.'
		else:
			datc='The planets with the lowest Equilibrium Temperature found are called '+", ".join(cold)+" and they're aprox. "+str(min(data[data.pl_eqt.isnull()==False].pl_eqt))+' Kelvins.'
		if len(hot)<2:
			dath='The planet with the highest Equilibrium Temperature found is called '+hot[0]+" and it's aprox. "+str(max(data[data.pl_eqt.isnull()==False].pl_eqt))+' Kelvins.'
		else:
			dath='The planets with the highest Equilibrium Temperature found are called '+", ".join(hot)+" and they're aprox. "+str(max(data[data.pl_eqt.isnull()==False].pl_eqt))+' Kelvins.'
			
		nucl="An example of a planetary structure: \n\nTerrestrial spherical shells layers can be divided (by density difference), an outer silicate solid crust, a highly viscous asthenosphere and mantle, a liquid outer core that is much less viscous than the mantle, and a solid inner core. \n\nBeyond all appearances, the shells are not perfect, but irregular joints. But classifying is always useful to try to understand our reality."
		
		info['temp_eqt']={'title': "What is Planetary Equilibrium Temperature?", 'content': file.read()+'\n\n'+datc+'\n'+dath+'\n\n'+nucl}
		file.close()
	
	if 'chz' in ask: #Zone of habitability
		file=open('HelpBob/Habitable_Zone.txt')
		info['chz']={'title': "What is Circumstellar Habitable Zone (CHZ)?", 'content': file.read()}
		file.close()
	
	if 'plsystem' in ask: #Planetary system, like the solar system.
		file=open('HelpBob/plt_system.txt')
		info['planet_system']={'title': "What is Planetary System?", 'content': file.read()}
		file.close()
		
	if 'clastar' in ask:  #How are stars categorized (Spectral Type)?
		file=open('HelpBob/stellar_clasification.txt')
		info['star_clasification']={'title': "How are stars categorized (Spectral Type)?", 'content': file.read()}
		file.close()
		
	if 'universal_age' in ask: #Ages of the Universe
		file=open('HelpBob/age_universe.txt')
		info['universal_age']={'title': "Ages and more ages: ", 'content': file.read()}
		file.close()

	return info

def whopl(**filt): #Planets filtered by conditions
	datu=data[:]
	if 'st_dist' in filt.keys():
		datu=datu[datu.st_dist==filt['st_dist']]
	if 'st_age' in filt.keys():
		datu=datu[datu.st_age==filt['st_age']]
	if 'st_spstr' in filt.keys():
		datu=datu[datu.st_spstr==filt['st_spstr']]
	if 'pl_facility' in filt.keys():
		datu=datu[datu.pl_facility==filt['pl_facility']]
	if 'pl_disc' in filt.keys():
		datu=datu[datu.pl_disc==filt['pl_disc']]
	if 'pl_locale' in filt.keys():
		datu=datu[datu.pl_locale==filt['pl_locale']]
	if 'pl_telescope' in filt.keys():
		datu=datu[datu.pl_telescope==filt['pl_telescope']]
	if 'pl_instrument' in filt.keys():
		datu=datu[datu.pl_instrument==filt['pl_instrument']]
	if 'pl_pnum' in filt.keys():
		datu=datu[datu.pl_pnum==filt['pl_pnum']]
	if 'pl_mnum' in filt.keys():
		datu=datu[datu.pl_mnum==filt['pl_mnum']]
	
	#Mass, radius, density
	if 'mmax' in filt.keys():
		datu=datu[datu.pl_bmassj<filt['mmax']]
	if 'mmin' in filt.keys():
		datu=datu[datu.pl_bmassj>filt['mmin']]
	if 'rmax' in filt.keys():
		datu=datu[datu.pl_rade<filt['rmax']]
	if 'rmin' in filt.keys():
		datu=datu[datu.pl_rade>filt['rmin']]
	if 'dmax' in filt.keys():
		datu=datu[datu.pl_dens<filt['dmax']]
	if 'dmin' in filt.keys():
		datu=datu[datu.pl_dens>filt['dmin']]

	return list(datu.pl_name)