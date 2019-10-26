# NASA-Space-APP_Backend
Backend for planetary construction project

Repository to manage the database of exoplanets of the nasa.Repository to manage the database of exoplanets of the nasa.

Description of the modules:

* exoplanets.py extracts the data securely; it also has a syntax error corrector.
    Dependencies: Pandas (Python Data Analysis Library), requests
    
    Sintax:
        
        Download in memory, data in Json format:
        
            exoplanets.get(table_of_data, tuple_of_number_colum, column1,...,columnN)
            
        Update dataset:
            
            exoplanets.update([table_of_data, tuple_of_number_colum, column1,...,columnN]) or exoplanets.update()

    Examples:
    
        exoplanets.get('exoplanets', (0,1), ['pl_hostname', 'pl_letter'], ['pl_name', 'pl_mnum'])
        
        exoplanets.update(['exoplanets', (0,1), ['pl_hostname', 'pl_letter'], ['pl_name', 'pl_mnum']])
    
* HelpBob.py Intriguing data of exoplanets for didactic use.
    Dependencies: Pandas (Python Data Analysis Library)

    Syntax: 
        
        Visualize star data (Distance, age, type) or planet (Links, planetary system moons, planetary system planets, Discovery information:   Year, installation, instrument and telescope): 

        HelpBob.opt('name_planet/name_star', 0/1, 'ID code data 1', 'ID code data 2')
        
        Access to informative texts, astronomical curiosities and definitions. Format Title, Content. Exoplanets, parsecs, Gyr, core, mantle, earth's crust, effective temperature, equilibrium temperature, habitability zone, spectral type, and so on:
        
        HelpBob.quest('Text code 1', 'Text code 2')
        
        Planet filter (By distance, star type, star age [age of the planetary system], maximum mass, minimum mass, radius, and so on):
        
        HelpBob.whopl(Key_name_a=number/string, key_name_b=number/string)
        
    Examples:
        
        HelpBob.opt('GJ 3021 b', 1, 'pl_pelink')    #Link Information
        
        HelpBob.quest('whatexo')    #Information "What is Exoplanet?"
        
        HelpBob.opt(whopl, st_age=2, mmax=32)   #Plantets with stars of 2 Gyr old, and less to 32 (Jupiter mass)
        
        
* Limits.py Analysis of realistic limitations of mass, volume, density, zone of habitability. Tools for preventive analysis to avoid collisions in orbits.
