"""  title= Plot Air Temperature """
"""  category= Atmosphere Data"""
"""  description= Test plotting MapExplorer Data  """
"""  app= Leonardo """
"""  context= all """
"""  output= PLT """


import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd     
                                   
from io import StringIO
                                    
   
from envimet import svgimage

# just for easier access convert sys var (Variant) to Python var
source=datafile.value                             
             
                                                
print ('File= '+source)                
print ('----------------------------------------------------')
                         
print('>> Reading '+source+' into Python Pandas...')          
df = pd.read_csv(source, sep=",", parse_dates=['DateTime'], index_col=['DateTime'])     
                
# print out the basic info of the dataframe 
print (df.info())    

print ('Basic Structure:')                  
print (df.head())      

### now we can do further processings on the dataframe 
                                   
        
                                  
                                           

figfile = StringIO()

#we should make sure we have a plain plot context, so let's clear it
plt.clf()
        
fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis
ax.scatter(df.index.values,
        df['Potential Air Temperature'],
        color='purple')
                              
                       
ax.set(xlabel="Date",
       ylabel="Air Temperature °C",
       title="Air Temperature at point")
                                             
# Rotate tick marks on x-axis
plt.setp(ax.get_xticklabels(), rotation=45)

                                   
                       
                       
                                
plt.show()


# proper exit code 
scriptresult.value= +1         
                  