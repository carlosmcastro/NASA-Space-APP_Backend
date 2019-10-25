#encoding: utf-8
#!/usr/bin/env python
#Modulo de información de la mascota alienigena Bob.

#Ejemplo de uso: Curiosidades.opt('GJ 3021 b', 'pl_pelink')
#NO MEZCLAR DATOS DE ESTRELLAS CON DATOS DE PLANETAS.
import pandas as pd

data=pd.read_csv('total_data.csv')

#Se han limpiado los datos de sistemas estelares binarios.
data=data.drop(data.loc[data['pl_cbflag']==1].index)

#Astro es el nombre de la estrella para st_dist.
#Astro es el nombre de un planeta para los demás casos.
def opt(astro, *args):
	info={}
	if (int(data.loc[data['pl_name']==astro].pl_kepflag)==1) or (int(data.loc[data['pl_name']==astro].pl_k2flag)==1):
		if ('pl_kepflag' in args) or ('pl_k2flag' in args):	#Si es dato de la mision kepler 1 o K2.
			file=open('HelpBob/Mision_Kepler.txt')
			misi=[file.read(), "https://www.nasa.gov/mission_pages/kepler/main/index.html", "https://es.wikipedia.org/wiki/Kepler_(sat%C3%A9lite)#Segunda_Luz_(K2)"]
			file.close()
			info['kepler']=misi
	if 'st_dist' in args:      	#Distancia del sistema al nuestro (parsecs)
		info['distancia']=data.loc[data['pl_hostname']==astro].st_dist
			
	if 'st_age' in args:      	#Edad de la estrella en Gyrs, billones de años.
		info['age']=[data.loc[data['pl_hostname']==astro].st_age, str(data.loc[data['pl_hostname']==astro].st_age/4.6)+' la edad del sol.']	
	if 'pl_facility' in args:	#Nombre de la instalación de observaciones de descubrimiento de planetas.
		info['instalacion']=data.loc[data['pl_name']==astro].pl_facility
	if 'pl_disc' in args:		#Año de descubrimiento planeta
		info['year']=data.loc[data['pl_name']==astro].pl_disc
	if 'pl_locale' in args:		#Lugar en que se descubrio el planeta
		info['lugar']=data.loc[data['pl_name']==astro].pl_locale
	if 'pl_telescope' in args:	#Telescopio que descubrio el planeta
		info['telescopio']=data.loc[data['pl_name']==astro].pl_telescope
	if 'pl_instrument' in args:	#Instrumento de descubrimiento de planetas.
		info['instrument']=data.loc[data['pl_name']==astro].pl_instrument
	if 'pl_mnum' in args:		#Número de lunas en el sistema planetario
		info['lunas']=data.loc[data['pl_name']==astro].pl_mnum
	if 'pl_pnum' in args:
		info['planet_number']=list(set(data.loc[data['pl_hostname']==astro].pl_pnum))[0]
	if 'pl_pelink' in args:		#Vincula a la pagina de enciclopedia exoplaneta.
		info['links']=['https://exoplanets.nasa.gov/' ,data.loc[data['pl_name']==astro].pl_pelink]
		if 'pl_edelink' in args:		#Vincula a otra pagina de enciclopedia exoplaneta.
			info['links'].append(data.loc[data['pl_name']==astro].pl_edelink)
	if 'st_spstr' in args:				#Da la clasificación de la estrella.
		tata=''
		morgank=str(list(data.loc[data['pl_hostname']==astro].st_spstr)[0])
		#Letras:
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
		
		#Números romanos.
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
			
		info['MK']=[morgank,tata] #Tipo de estrella en notación y en lenguaje comun
	return info
	
def quest(*ask):
	info={}
	if 'whatexo' in ask: #¿Que es un exoplaneta? Definición de parsecs, planeta y exoplaneta más cercano y lejano
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
			datf='The nearest exoplanets found are called '+", ".join(farth)+" and they're aprox. "+str(max(data.st_dist))+' parsecs away.'
		
		#calculos realizados con NASA's Juno spacecraft
		parse="To travel a parsec distance would take about 3.26 years at the speed of light. Our fastest rocket built would take about 9651 years."

		info['exo_definition']={'title': 'What is an exoplanet?', 'content': file.read()+'\n\n'+datn+'\n'+datf+'\n\n'+parse}
		file.close()
	
	if 'claexo' in ask: #Información sobre la clasificación de estrellas y planetas.
		file=open('HelpBob/names_exoplanets.txt')
		info['exo_clasification']={'title': 'Exoplanet naming convention', 'content': file.read()}
		file.close()
	
	if 'teff' in ask: #Temperatura efectiva de estrella.
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
	
	if 'teeqt' in ask: #Temperatura de equilibrio de un planeta. Breve descripción de la estructura de la Tierra.
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
	
	if 'chz' in ask: #Zona de habitabilidad
		file=open('HelpBob/Habitable_Zone.txt')
		info['chz']={'title': "What is Circumstellar Habitable Zone (CHZ)?", 'content': file.read()}
		file.close()
	
	if 'plsystem' in ask: #Sistema planetario, como el sistema solar.
		file=open('HelpBob/plt_system.txt')
		info['planet_system']={'title': "What is Planetary System?", 'content': file.read()}
		file.close()
		
	if 'clastar' in ask:
		file=open('HelpBob/stellar_clasification.txt')
		info['star_clasification']={'title': "How are stars categorized (Spectral Type)?", 'content': file.read()}
		file.close()
		
	if 'universal_age' in ask:
		file=open('HelpBob/age_universe.txt')
		info['universal_age']={'title': "Ages and more ages: ", 'content': file.read()}
		file.close()
	
	return info
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	