"""" title=Surface Energy """
"""" category=Surface  """
"""" description=Plotting the surface energy balance """
"""" app=Leonardo """
"""" context=GridExplor_FX """
"""" output=svg """
"""" datafile1=Time Series Surface  """

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from io import StringIO
                                    
   
# from envimet import svgimage

# just for easier access convert sys var (Variant) to Python var
# source=datafile.value                             
source =  '/Users/takaimasaichi/Desktop/cslTakai/RadiationAndWindWR/surface/New Simulation_FX_2021-08-06_10.00.00.EDT'          
                        
                                                
print ('File= '+source)                
print ('----------------------------------------------------')
                         
print('>> Reading '+source+' into Python Pandas...')          
df = pd.read_csv(source, sep=",", parse_dates=['DateTime'], index_col=['DateTime'],encoding='ISO-8859-1')     
                
# print out the basic info of the dataframe 
print (df.info())    

print ('Basic Structure:')                  
print (df.head())      

### now we can do further processings on the dataframe 
figfile = StringIO()

 
        
fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis              
ax.plot(df.index.values,
        df["Q_Sw Direct"],
        color='purple',   
        marker='o',
        label='Shortwave direct')
                        
ax.plot(df.index.values,  
        df["Q_Sw Diffuse Horizontal"],
        color='orange',
        label='Shortwave diffuse')

ax.plot(df.index.values,  
        df["Sensible heat flux"],
        color='blue',       
        label='Sensible Heat Flux H')
                              
ax.plot(df.index.values,                        
        df["Latent heat flux"],
        color='green',                  
        label='Latent Heat Flux LE')
        
ax.plot(df.index.values,  
        df["Soil heat Flux"],
        color='brown',      
        marker='x',
        label='Soil Heat Flux G')
        
        
                              
                       
ax.set(xlabel="Date",
       ylabel="Surface Energy Components",
       title="Surface Energy")     
       
       
       
ax.legend()
       
                                             
# Rotate tick marks on x-axis
plt.setp(ax.get_xticklabels(), rotation=45)

                                   
                       
plt.savefig(figfile, format='svg')

figdata_svg= figfile.getvalue()
svgimage.SvgText= figdata_svg  


# proper exit code 
scriptresult.value= +1         
