"""" title=Dash-Demo_ScenarioComparison """
"""" category=Atmosphere Data """
"""" description=This script takes one area, a data index and two files as input and creates a comparison as HTML-site """
"""" app=Leonardo """                                            
"""" context=GridExplor_AT,GridExplor_FX,GridExplor_SO,GridExplor_POLU,GridExplor_VEG,GridExplor_RD """
"""" output=html """         

from envimet import DataFile
from envimet import EDXfile
from envimet import EDXfileSeries
import numpy as np
import matplotlib.pyplot as plt

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd

# settings  
x_from = 50
x_to = 60
y_from = 30
y_to = 50
z_from = 4
z_to = 4   

time_from = 0
time_to = 10                       
                                                                                   
data_index = 8
                                                                                          
file_1 = 'D:/enviprojects/Leonardo_Scripts_DummyProject/DummyProject_Leonardo_output/atmosphere/DummyProject_Leonardo_AT_2018-06-23_10.00.01.EDX'     
scenario_1 = 'D:/enviprojects/Leonardo_Scripts_DummyProject/DummyProject_Leonardo_output/atmosphere'    

file_2 = 'D:/enviprojects/Leonardo_Scripts_DummyProject_Scen2/DummyProject_Leonardo_Scen2_output/atmosphere/DummyProject_Leonardo_Scen2_AT_2018-06-23_10.00.01.EDX'     
scenario_2 = 'D:/enviprojects/Leonardo_Scripts_DummyProject_Scen2/DummyProject_Leonardo_Scen2_output/atmosphere'         
# end of settings                                     
    
# initialize                         
data1 = np.empty([abs(time_to - time_from)+1, (abs(x_to - x_from)+1)*(abs(y_to - y_from)+1)*(abs(z_to - z_from)+1)], dtype = float) 
data2 = np.empty([abs(time_to - time_from)+1, (abs(x_to - x_from)+1)*(abs(y_to - y_from)+1)*(abs(z_to - z_from)+1)], dtype = float) 
timesteps = []
date = []
                                                
EDXfile.ReadFile(file_1) 
EDXfileSeries.ReadFolder(scenario_1, EDXfile.SimBaseID)

DataFile.SetEDXfileInSeries(EDXfileSeries, time_from)
startDate = DataFile.associatedEDXFile.simdate
DataFile.SetEDXfileInSeries(EDXfileSeries, time_to)
endDate = DataFile.associatedEDXFile.simdate

# print and save variable names and units
for i in range(0, DataFile.GetLenOfNameVars()):
    print(str(i) + ': ' + DataFile.GetVarNameAndUnit(i))

for t in range(0, abs(time_to - time_from)+1):                 
    DataFile.SetEDXfileInSeries(EDXfileSeries, t + time_from) 
    timesteps.append(DataFile.associatedEDXFile.simtime[0:2])
    date.append(DataFile.associatedEDXFile.simdate + ' ' + DataFile.associatedEDXFile.simtime[0:2])   
    x = 0
    for i in range(0, abs(x_to - x_from)+1):                           
        for j in range(0, abs(y_to - y_from)+1):
            for k in range(0, abs(z_to - z_from)+1):  
                data1[t][x] = DataFile.GetDataPointValue(data_index, i + x_from, j + y_from, k + z_from)
                x += 1
    
EDXfile.ReadFile(file_2) 
EDXfileSeries.ReadFolder(scenario_2, EDXfile.SimBaseID)

for t in range(0, abs(time_to - time_from)+1):                 
    DataFile.SetEDXfileInSeries(EDXfileSeries, t + time_from)     
    x = 0
    for i in range(0, abs(x_to - x_from)+1):                           
        for j in range(0, abs(y_to - y_from)+1):
            for k in range(0, abs(z_to - z_from)+1):  
                data2[t][x] = DataFile.GetDataPointValue(data_index, i + x_from, j + y_from, k + z_from)
                x += 1            
            

#min_vals1 = np.nanmin(data1, axis=1)
#max_vals1 = np.nanmax(data1, axis=1)
mean_vals1 = np.nanmean(data1, axis=1)

#min_vals2 = np.nanmin(data2, axis=1)
#max_vals2 = np.nanmax(data2, axis=1)
mean_vals2 = np.nanmean(data2, axis=1)

diff_vals = np.empty(mean_vals1.size, dtype=float)
for i in range(0, diff_vals.size):
    diff_vals[i] = abs(mean_vals1[i] - mean_vals2[i])

a = np.empty([mean_vals1.size, 2], dtype = float) 
for i in range(0, mean_vals1.size):
    for j in range(0,3):
        if j == 0:
            a[i][j] = mean_vals1[i]
        if j == 1:
            a[i][j] = mean_vals2[i]


#a = np.empty([min_vals1.size, 3], dtype = float) 
#for i in range(0, min_vals1.size):
#    for j in range(0,3):
#        if j == 0:
#            a[i][j] = min_vals1[i]
#        if j == 1:
#            a[i][j] = max_vals1[i]
#        if j == 2:
#            a[i][j] = mean_vals1[i]
            

df_data1 = pd.DataFrame(data=np.nanmean(data1, axis=1), index=timesteps)

#diff_vals = np.empty(min_vals1.size, dtype=float)
#for i in range(0, diff_vals.size):
#    diff_vals[i] = max_vals1[i] - min_vals1[i]


df_a = pd.DataFrame(data=a, index=timesteps, columns=['mean Scenario A','mean Scenario B'])
df_dt = pd.DataFrame(data=date, columns=['date'])
df_a.index = pd.to_datetime(df_dt['date'])
df_a.to_csv(path_or_buf='D:/data_df.csv', columns=['mean Scenario A','mean Scenario B'], index=True, sep=';')

df_diff = pd.DataFrame(data=diff_vals, columns=['Difference between Scenarios'])
df_diff.index = pd.to_datetime(df_dt['date'])
df_diff.to_csv(path_or_buf='D:/diff_df.csv', columns=['Difference between Scenarios'], index=True, sep=';')


#df = pd.read_csv('D:/data.csv', delimiter=';')
df = pd.read_csv('D:/data_df.csv', delimiter=';', header=0, index_col=0)
#df.index = pd.to_datetime(df['date'])
diff = pd.read_csv('D:/diff_df.csv', delimiter=';', header=0, index_col=0)
app = dash.Dash(__name__)

app.layout = html.Div(children=[html.Div(className='row',
                                         children=[html.Div(className='Text-Div',
                                                            children=[
                                                                html.H2('ENVI-met Dash Demo'),
                                                                html.P('Visualising ENVI-met Data with Dash'),
                                                            ]),
                                                   html.Div(className='Data-Div',
                                                            children=[
                                                                dcc.Graph(id='timeseries',
                                                                          config={'displayModeBar': False},
                                                                          animate=True,
                                                                          figure=px.line(df,
                                                                                         labels={
                                                                                             'date': 'Date',
                                                                                             'value': 'Temperature [ﾂｰC]'
                                                                                         },
                                                                                         title='Comparison of Potential Air Temperature between Scenario A and Scenario B')
                                                                )]),
                                                   html.Div(className='Bar-Plot-Div',
                                                            children=[
                                                                dcc.Graph(id='barplot',
                                                                          config={'displayModeBar': True},
                                                                          animate=True,
                                                                          figure=px.bar(diff,
                                                                                        labels={
                                                                                            'date': 'Date',
                                                                                            'value': 'Temperature [ﾂｰC]'
                                                                                        },
                                                                                        title='Absolute difference between Scenario A and Scenario B'
                                                                          ))
                                                            ]),
                                                   html.Footer(className='Footer',
                                                               children=[
                                                                   html.P('Created with ENVI-met DataCenter & Plotly Dash')
                                                               ])
                                                   ])
                                ])

app.run_server(debug=True)