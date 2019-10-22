#encoding: utf-8
#!/usr/bin/env python

#Ejemplo de uso: Curiosidades.opt('GJ 3021 b', 'pl_pelink')
#NO MEZCLAR DATOS DE ESTRELLAS CON DATOS DE PLANETAS.
import pandas as pd

data=pd.read_csv('total_data.csv')

#Se han limpiado los datos de sistemas estelares binarios.
data=data.drop(data.loc[data['pl_cbflag']==1].index)

def opt(astro, *args):
	info={}
	if (int(data.loc[data['pl_name']==astro].pl_kepflag)==1) or (int(data.loc[data['pl_name']==astro].pl_k2flag)==1):
		if ('pl_kepflag' in args) or ('pl_k2flag' in args):	#Si es dato de la mision kepler 1 o K2.
			file=open('Mision_Kepler')
			misi=[file.read(), "https://www.nasa.gov/mission_pages/kepler/main/index.html", "https://es.wikipedia.org/wiki/Kepler_(sat%C3%A9lite)#Segunda_Luz_(K2)"]
			info['kepler']=misi
	if 'st_dist' in args:      	#Distancia del sistema al nuestro (parsecs)
		info['distancia']=data.loc[data['st_hostname']==astro].st_dist
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
	if 'pl_pelink' in args:		#Vincula a la pagina de enciclopedia exoplaneta.
		info['link']=data.loc[data['pl_name']==astro].pl_pelink
	return info