"""" title=Compare Locations"""
"""" category=Atmosphere Data """
"""" description=This script takes two areas, a file path and a data index as input and creates a comparison between these two areas for the selected variable """
"""" app=Leonardo """
"""" context=GridExplor_AT,GridExplor_POLU """
"""" output=generic """      

from envimet import DataFile
from envimet import EDXfile
from envimet import EDXfileSeries
import numpy as np
import matplotlib.pyplot as plt

# settings - defined by the user

# define Location A (as bounding box)
x1_from = 9
x1_to = 27
y1_from = 37
y1_to = 47
z1_from = 4
z1_to = 4  

# define Location B (as bounding box)
x2_from = 47
x2_to = 56
y2_from = 30
y2_to = 48
z2_from = 4
z2_to = 4     

# define the timespan you would like to compare - index in folder 
# our sample simulation started at 23.06.2018 07:00h, so our first EDX-output file is 08:00h. If we now set "time_from" to 0, we start at the 08:00h file, since it is the first output file (index 0)
# set "time_from = 1" to start with the second output file, which would be 09:00h in our case
# "time_to = 92" means, that the last file you would like to analyse ist the 93 EDX-file in the folder
time_from = 0
time_to = 92                       

# define the data you want to compare -> data-indexes are printed in the console when the script runs
# if you would like to analyse an other variable, run the script and have a look at the console, which prints the indexes                                                                                    
data_index = 8
                                                                                                   
# end of settings                                     

# helper functions
identity = lambda x: x

# a=from, b=to, x=steps
def getDates(a, b, x):
    res = []
    for index in range(a, b+1, x):
        DataFile.SetEDXfileInSeries(EDXfileSeries, index)
        res.append(DataFile.associatedEDXFile.simdate)
    return res
    
# initialize  

# load selected files and folders 
# define the file and filepath for scenario 1
file = datafile.value     
folder = file[0:(len(file) - len(file.split("\\")[-1]))]   

# initialize - create empty arrays to store the data in the following (data1 for location A and data2 for location B)
# we use numpy arrays (np) because they are much faster                       
data1 = np.empty([abs(time_to - time_from)+1, (abs(x1_to - x1_from)+1)*(abs(y1_to - y1_from)+1)*(abs(z1_to - z1_from)+1)], dtype = float) 
data2 = np.empty([abs(time_to - time_from)+1, (abs(x2_to - x2_from)+1)*(abs(y2_to - y2_from)+1)*(abs(z2_to - z2_from)+1)], dtype = float) 
timesteps = []

# load EDX-file
# here we use implemented functions in the ENVI-met source code to directly access the data from the EDX-files 
# first, we need to read the EDX-file and -folder                                                 
EDXfile.ReadFile(file) 
EDXfileSeries.ReadFolder(folder, EDXfile.SimBaseID)
# now we set a EDX-file with the following command. "time_from" is the index of files in the folder
# since "time_from" is 0, we would like to set the first EDX file in the series 
DataFile.SetEDXfileInSeries(EDXfileSeries, time_from)
# done - now we can access the simulation date of this timestep 
startDate = DataFile.associatedEDXFile.simdate
# same for the last file we would like to analyse
# To do so, just set the EDX-file at index "time_to"
DataFile.SetEDXfileInSeries(EDXfileSeries, time_to)
# ... and read the simulation date again
endDate = DataFile.associatedEDXFile.simdate
# now we got our simulation start- and end-date 

# print and save variable names and units
for i in range(0, DataFile.GetLenOfNameVars()):
    print(str(i) + ': ' + DataFile.GetVarNameAndUnit(i))

# load data from both locations and fill timesteps 
xTick_labels = []
for t in range(0, abs(time_to - time_from)+1):                 
    DataFile.SetEDXfileInSeries(EDXfileSeries, t + time_from) 
    xTick_labels.append(DataFile.associatedEDXFile.simtime[0:2])
    timesteps.append(str(t))
    x = 0
    for i in range(0, abs(x1_to - x1_from)+1):                           
        for j in range(0, abs(y1_to - y1_from)+1):
            for k in range(0, abs(z1_to - z1_from)+1):  
                data1[t][x] = DataFile.GetDataPointValue(data_index, i + x1_from, j + y1_from, k + z1_from)
                x += 1
    x = 0
    for i in range(0, abs(x2_to - x2_from)+1):                           
        for j in range(0, abs(y2_to - y2_from)+1):
            for k in range(0, abs(z2_to - z2_from)+1):  
                data2[t][x] = DataFile.GetDataPointValue(data_index, i + x2_from, j + y2_from, k + z2_from)
                x += 1            
            

# calculate minimum, maximum and mean values for each timestep at each location
min_vals1 = np.nanmin(data1, axis=1)
max_vals1 = np.nanmax(data1, axis=1)
mean_vals1 = np.nanmean(data1, axis=1)

min_vals2 = np.nanmin(data2, axis=1)
max_vals2 = np.nanmax(data2, axis=1)
mean_vals2 = np.nanmean(data2, axis=1)

# now we calculate the absolute difference for every timestep
diff_vals = np.empty(mean_vals1.size, dtype=float)
for i in range(0, diff_vals.size):
    diff_vals[i] = abs(mean_vals1[i] - mean_vals2[i])

# the data is now ready for the plot

#plots
#plot 1 - simple comparison of both locations (Location A in upper figure and Location B in lower figure)
if diagramtitle.value == '':
    dTitle = 'Comparison of ' + DataFile.GetVarNameAndUnit(data_index) + ' between location A and B'
else:
    dTitle = diagramtitle.value

# define general plot-settings
figure = plt.figure(facecolor="lightsteelblue")
# with "ori" we mean the orientation of our script
# the number is composed as follows: 
# first number: number of rows
# second number: number of columns 
# third number: number of plots - the third number gets increased step by step
# until now, we got 0 plots in our composition
ori = 210 # 2 rows, 1 column
plots1 = [[],[]]
# now we add the plots iteratively  
count = 1
for i in plots1:
    i.append(figure.add_subplot(ori + count))
    count += 1

# define first plot (direct comparison)
ax1 = plots1[0][0]
ax1.plot(timesteps, min_vals1, color='blue', label='Minimum values')
ax1.plot(timesteps, max_vals1, color='red', label='Maximum values')
ax1.plot(timesteps, mean_vals1, color='green', label='Mean values')
ax1.fill_between(timesteps, max_vals1, min_vals1, alpha=0.2)
if startDate != endDate:
    ax1.set(xlabel='timesteps [h]', ylabel=DataFile.GetVarNameAndUnit(data_index), title='Location A : ' + DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + endDate + ' ' + xTick_labels[-1] + ':00h)')
else:
    ax1.set(xlabel='timesteps [h]', ylabel=DataFile.GetVarNameAndUnit(data_index), title='Location A : ' + DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + xTick_labels[-1] + ':00h)')
ax1.legend(loc="upper right")
ax1.grid()

ax1.set_xticklabels(xTick_labels)
for label in ax1.xaxis.get_ticklabels()[1::2]:
    label.set_visible(False)
    
secax = ax1.secondary_xaxis('top', functions=(identity, identity))
secax.set_xticklabels(getDates(time_from, time_to, 24))

secax.set_xticks(np.arange(time_from, time_to, step=24))

for i in range(len(xTick_labels)):
    if xTick_labels[i] == '00':
        ax1.axvline(x=timesteps[i])

ax1 = plots1[1][0]
ax1.plot(timesteps, min_vals2, color='blue', label='Minimum values')
ax1.plot(timesteps, max_vals2, color='red', label='Maximum values')
ax1.plot(timesteps, mean_vals2, color='green', label='Mean values')
ax1.fill_between(timesteps, max_vals2, min_vals2, alpha=0.2)
if startDate != endDate:
    ax1.set(xlabel='timesteps [h]', ylabel=DataFile.GetVarNameAndUnit(data_index), title='Location B : ' + DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + endDate + ' ' + xTick_labels[-1] + ':00h)')
else:
    ax1.set(xlabel='timesteps [h]', ylabel=DataFile.GetVarNameAndUnit(data_index), title='Location B : ' + DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + xTick_labels[-1] + ':00h)')
ax1.legend(loc="upper right")
ax1.grid()

for i in range(len(xTick_labels)):
    if xTick_labels[i] == '00':
        ax1.axvline(x=timesteps[i])

for label in ax1.xaxis.get_ticklabels()[1::2]:
    label.set_visible(False)
    
figure.suptitle(dTitle)
figure.set_size_inches(20, 20)
plt.xticks(timesteps, xTick_labels)
plt.rcParams["figure.figsize"] = (75, 50)
plt.subplots_adjust(left = 0.125, right = 0.9, bottom = 0.1, top = 0.9, wspace = 0.2, hspace = 0.3)
plt.show()      

# plot 2 - comparison of mean values between both locations in upper plot and absolute difference between these mean values plotted in lower figure                                                          
if diagramtitle.value == '':
    dTitle = 'Comparison of ' + DataFile.GetVarNameAndUnit(data_index) + ' between location A and B'
else:
    dTitle = diagramtitle.value

figure2 = plt.figure(facecolor="lightsteelblue")
plots2 = [[],[]]
count = 1

for i in plots2:
    i.append(figure2.add_subplot(ori + count))
    count += 1
    
ax2 = plots2[0][0]
# we would like to plot the mean values for both scenarios in the same graph.
# Hence, we call the plot-function two times, first with the mean values from Location A and second with the mean values from Location B
ax2.plot(timesteps, mean_vals1, color='green', label= 'Mean values Location A')
ax2.plot(timesteps, mean_vals2, color='blue', label= 'Mean values Location B ')
# to visualize the gap, we fill the area between both graphs 
ax2.fill_between(timesteps, mean_vals1, mean_vals2, alpha=0.2)
# now we set the title of out first figure in the second plot.
if startDate != endDate:
    ax2.set(xlabel='timesteps [h]', ylabel=DataFile.GetVarNameAndUnit(data_index), title= DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + endDate + ' ' + xTick_labels[-1] + ':00h)')
else:
    ax2.set(xlabel='timesteps [h]', ylabel=DataFile.GetVarNameAndUnit(data_index), title= DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + xTick_labels[-1] + ':00h)')
    
# ... place the legend in the upper right corner 
ax2.legend(loc="upper right")
# ... add a grid to our plot
ax2.grid()
# set the labels for our x-axis (to show the timestep and not the file-index)
ax2.set_xticklabels(xTick_labels)
for label in ax2.xaxis.get_ticklabels()[1::2]:
    label.set_visible(False)
# now we define a secondary axis, where the date of the corresponding day is shown    
secax = ax2.secondary_xaxis('top', functions=(identity, identity))
secax.set_xticklabels(getDates(time_from, time_to, 24))
# it is enough to show the date once every 24 hours, so we set setp = 24
secax.set_xticks(np.arange(time_from, time_to, step=24))
# To visualize that we plot multiple days, we add a vertical line every time the timestep is 00:00h
for i in range(len(xTick_labels)):
    if xTick_labels[i] == '00':
        ax2.axvline(x=timesteps[i])
        
# define second figure (absolute difference)        
ax2 = plots2[1][0]
# our second plot is a bar plot. Here we set the zorder = 3 to display the bars in the foreground
ax2.bar(timesteps, diff_vals, zorder=3)

# set the title for the second figure
if startDate != endDate:
    ax2.set(xlabel='timesteps [h]', ylabel='Absolute Difference ' + DataFile.GetVarNameAndUnit(data_index), title= 'Absolute Difference ' + DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + endDate + ' ' + xTick_labels[-1] + ':00h)')
else:
    ax2.set(xlabel='timesteps [h]', ylabel='Absolute Difference ' + DataFile.GetVarNameAndUnit(data_index), title= 'Absolute Difference ' + DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + xTick_labels[-1] + ':00h)')

# ... add a grid (zorder=0 to display the grid in the background)
ax2.grid(zorder=0)
# add vertical lines again 
for i in range(len(xTick_labels)):
    if xTick_labels[i] == '00':
        ax2.axvline(x=timesteps[i])
        
for label in ax2.xaxis.get_ticklabels()[1::2]:
    label.set_visible(False)
# set the title and size the plots
figure2.suptitle(dTitle)
figure2.set_size_inches(20, 20)
plt.xticks(timesteps, xTick_labels)
plt.rcParams["figure.figsize"] = (75, 50)   
plt.subplots_adjust(left = 0.125, right = 0.9, bottom = 0.1, top = 0.9, wspace = 0.2, hspace = 0.3)
# show the result 
plt.show()