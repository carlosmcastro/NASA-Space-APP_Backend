#encoding: utf-8
#!/usr/bin/env python
#Más información: https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html
#Uso de API NASA Exoplanet Archive; para optimizar la visualización de datos de Planetas Confirmados.
#No incluye filtrado por fechas, ni uso de comodines.

#Uso exoplanets.get(tabla_de_datos, conjunto_de_columnas, columnas1,...,columnaN)
#Ejemplo: exoplanets.get('exoplanets', (0,1), ['pl_hostname', 'pl_letter'], ['pl_name', 'pl_mnum'])

#El script posee un corrector de errores, aproximando el nombre de la tabla y de las columnas a buscar.
#Es menos aproximado el dato corregido, cuando la palabra equivocada es corta, como por ejemplo poner "dic" en lugar de "dec"

#Solo se puede acceder a un conjunto de datos por conjunto de columnas, esto ocurre intencionalmente, para forzar la busqueda de datos precisos.

#El script devulve un dicciónario con datos Json.

import requests

api="https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?" #Parametro obligatorio

#tabla de Planetas confirmados (Obligatorio)
#tabla: (columnas)
tables={'exoplanets': (		#Confirmed Planets
					   ('pl_hostname', 'pl_letter', 'pl_name', 'pl_discmethod', 'pl_controvflag', #Default Columns
					   'pl_pnum', 'pl_orbper', 'pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 
					   'pl_bmassj', 'pl_bmassprov', 'pl_radj', 'pl_dens', 'pl_ttvflag', 
					   'pl_kepflag', 'pl_k2flag', 'pl_nnotes', 'ra_str', 'dec_str', 'ra', 
					   'dec', 'st_dist', 'gaia_dist', 'st_optmag', 'st_optband', 
					   'gaia_gmag', 'st_teff', 'st_mass', 'st_rad', 'rowupdate', 'pl_facility'),
					   ('pl_tranflag', 'pl_rvflag', 'pl_imgflag', 'pl_astflag', 'pl_omflag', 	  #Planet Columns
					   'pl_cbflag', 'pl_angsep', 'pl_orbtper', 'pl_orblper', 'pl_rvamp', 
					   'pl_eqt', 'pl_insol', 'pl_massj', 'pl_msinij', 'pl_masse', 
					   'pl_msinie', 'pl_bmasse', 'pl_rade', 'pl_rads', 'pl_trandep', 
					   'pl_trandur', 'pl_tranmid', 'pl_tsystemref', 'pl_imppar', 'pl_occdep', 
					   'pl_ratdor', 'pl_ratror', 'pl_def_refname', 'pl_disc', 'pl_disc_refname', 
					   'pl_locale', 'pl_telescope', 'pl_instrument', 'pl_status', 'pl_mnum', 
					   'pl_st_npar', 'pl_st_nref', 'pl_pelink', 'pl_edelink', 'pl_publ_date'),
					   ('hd_name', 'hip_name', 'st_rah', 'st_glon', 'st_glat', 					  #Stellar Columns
					   'st_elon', 'st_elat', 'st_plx', 'gaia_plx', 'st_pmra', 
					   'st_pmdec', 'st_pm', 'gaia_pmra', 'gaia_pmdec', 'gaia_pm', 
					   'st_radv', 'st_spstr', 'st_logg', 'st_lum', 'st_dens', 
					   'st_metfe', 'st_metratio', 'st_age', 'st_vsini', 'st_acts', 
					   'st_actr', 'st_actlx', 'swasp_id', 'st_nts', 'st_nplc', 
					   'st_nglc', 'st_nrvc', 'st_naxa', 'st_nimg', 'st_nspec'),
					   ('st_uj', 'st_vj', 'st_bj', 'st_rc', 'st_ic', 						       #Photometry Columns
					   'st_j', 'st_h', 'st_k', 'st_wise1', 'st_wise2', 
					   'st_wise3', 'st_wise4', 'st_irac1', 'st_irac2', 'st_irac3', 
					   'st_irac4', 'st_mips1', 'st_mips2', 'st_mips3', 'st_iras1', 
					   'st_iras2', 'st_iras3', 'st_iras4', 'st_photn'),
					   ('st_umbj', 'st_bmvj', 'st_vjmic', 'st_vjmrc', 'st_jmh2', 			       #Color Columns
					   'st_hmk2', 'st_jmk2', 'st_bmy', 'st_m1', 'st_c1', 'st_colorn')
					   ), 		
		'compositepars': (	 #Composite Planet Data
						('fpl_hostname', 'fpl_letter', 'fpl_name', 'fpl_discmethod', 'fpl_disc',   #Planet Parameters
						'fpl_controvflag', 'fpl_orbper', 'fpl_orbperreflink', 'fpl_smax', 'fpl_smaxreflink', 
						'fpl_eccen', 'fpl_eccenreflink', 'fpl_bmasse', 'fpl_bmassj', 'fpl_bmassprov', 
						'fpl_bmassreflink', 'fpl_rade', 'fpl_radj', 'fpl_rads', 'fpl_radreflink', 
						'fpl_dens', 'fpl_densreflink', 'fpl_eqt', 'pl_eqtreflink', 'fpl_insol', 
						'fpl_insolreflink', 'fpl_tranflag', 'fpl_cbflag'),
						('fpl_snum', 'ra_str', 'dec_str', 'ra', 'dec', 							   #Stellar Columns
						' fst_posreflink', 'fst_dist', 'fst_distreflink', 'fst_optmag', 'fst_optmagband', 
						'fst_optmagreflink', 'fst_nirmag', 'fst_nirmagband', 'fst_nirmagreflink', 'fst_spt', 
						'fst_sptreflink', 'fst_teff', 'fst_teffreflink', 'fst_logg', 'fst_loggreflink', 
						'fst_lum', 'fst_lumreflink', 'fst_mass', 'fst_massreflink', 'fst_rad', 
						'fst_radreflink', 'fst_met', 'fst_metratio', 'fst_metreflink', 'fst_age', 'fst_agereflink')
					   ),
		'exomultpars': (	#Extended Planet Data
						('mpl_hostname', 'mpl_letter', 'mpl_def', 'mpl_reflink', 'mpl_discmethod', #Default Columns
						'mpl_pnum', 'mpl_orbper', 'mpl_orbsmax', 'mpl_orbeccen', 'mpl_orbincl', 
						'mpl_bmassj', 'mpl_bmassprov', 'mpl_radj', 'mpl_dens', 'ra_str', 
						'dec_str', 'ra', 'dec', 'mst_teff', 'mst_mass', 'mst_rad', 'rowupdate'),
						('mpl_name', 'mpl_tranflag', 'mpl_rvflag', 'mpl_ttvflag', 'mpl_orbtper',   #Planet Columns
						'mpl_orblper', 'mpl_rvamp', 'mpl_eqt', 'mpl_insol', 'mpl_massj', 
						'mpl_msinij', 'mpl_masse', 'mpl_msinie', 'mpl_bmasse', 'mpl_rade', 
						'mpl_rads', 'mpl_trandep', 'mpl_trandur', 'mpl_tranmid', 'mpl_tsystemref', 
						'mpl_imppar', 'mpl_occdep', 'mpl_ratdor', 'mpl_ratror', 'mpl_disc', 
						'mpl_status', 'mpl_mnum', 'mpl_publ_date'),
						('hd_name', 'hip_name', 'mst_logg', 'mst_lum', 'mst_dens', 					#Stellar Columns
						'mst_metfe', 'mst_metratio', 'mst_age', 'swasp_id')
					   ),
		'microlensing': (	#Microlensing
						('plntname', 'ra_str', 'dec_str', 'mlmassplnj', 'mlmassplne', 				#Default Columns
						'mlsmaproj', 'mlmasslens', 'mldistl', 'mldists', 'mltsepmin', 
						'mlsepminnorm', 'mlxtimeein', 'mlradsnorm', 'mlsmaxpnorm', 'mlmassratio', 
						'mlangstlax', 'mlmagis', 'mlmagibl', 'mlradeinang', 'mlpmrells', 
						'mlmodeldef', 'plntreflink'),
						('ra', 'dec', 'glon', 'glat'),												#Coordinate Columns
						('mlplxrel', 'mlplxmicro', 'mlplxmicron', 'mlplxmicroe', 'mldsdt', 			#Microlensing Parameter Columns
						'mldalphadt', 'mlradsang', 'mlradsphy', 'mlxtimesrc', 'mlefftime', 'mlpms'),
						('mlmagvs', 'mlmagvso', 'mlmagiso', 'mlmagjs', 'mlmagjso', 					#Magnitude Columns
						'mlmaghs', 'mlmaghso', 'mlmagks', 'mlmagkso', 'mlmagibase', 
						'mlmagvl', 'mlmagil', 'mlmagjl', 'mlmaghl', 'mlmagkl', 
						'mlextvfld', 'mlextifld', 'mlextjfld', 'mlexthfld', 'mlextkfld'),
						('mlcolvis', 'mcolviso', 'mlcolvks', 'mlcolvkso', 'mlcolihs', 				#Color Columns
						'mlcolihso', 'mlcolhks', 'mlcolhkso', 'mlcolvibl', 'mlredvi', 
						'mlredvk', 'mlredhk'),
						('mlmodelchisq', 'mlcbflag', 'mldescription')								#Model Columns
						), 	
		} 

#Llamada a la API
def get(tabl, num, *args):
	if not tabl in tables.keys():
		tabla=concor(tabl, tables.keys())
	else:
		tabla=tabl
	columna=[]

#Comprueba las columnas.
	for une in range(len(num)):
		for col in args[une]:
			if not col in tables[tabla][num[une]]:
				columna.append(concor(col, tables[tabla][num[une]]))
			else:
				columna.append(col)

#Realiza la llamada.
	response=requests.get(api+'table='+tabla+'&select='+",".join(columna)+'&order=dec&format=json')
	if response:
		busqueda=response.json()
		response.close()
		return busqueda #Convert .csv: import pandas as pd, data=pd.DataFrame(busqueda)
	else:
		print('Ha ocurrido un error')
		
		
#Verifica los datos de busqueda reales, más cercanos.
def concor(dato, conjunto):
	similar={}
	for i in conjunto:
		similar[len(set(dato).intersection(set(i)))]=i
	return similar[max(similar.keys())]