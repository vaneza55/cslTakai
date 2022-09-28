"""" title=CompareScenarioData """
"""" category=Atmosphere Data """
"""" description=This script takes two different scenarios and compares the same location for a defined variable. """
"""" app=Leonardo """
"""" context=GridExplor_AT,GridExplor_POLU """
"""" output=Generic Python Output """

from envimet import DataFile
from envimet import EDXfile
from envimet import EDXfileSeries
import numpy as np
import matplotlib.pyplot as plt

# settings - defined by the user

# define the location you would like to compare (as bounding box)
x_from = 50
x_to = 60
y_from = 30
y_to = 50
z_from = 1
z_to = 4

# define the data you want to compare -> data-indexes are printed in the console when the script runs
# if you would like to analyse an other variable, run the script and have a look at the console, which prints the indexes 
data_index = 8

# define the timespan you would like to compare - index in folder 
# our sample simulation started at 23.06.2018 07:00h, so our first EDX-output file is 08:00h. If we now set "time_from" to 0, we start at the 08:00h file, since it is the first output file (index 0)
# set "time_from = 1" to start with the second output file, which would be 09:00h in our case
# "time_to = 30" means, that the last file you would like to analyse ist the 30 EDX-file in the folder
time_from = 0
time_to = 92

# optional parameter - just use them if your second scenario has not the same simulation period as your first scenario
# again the index needs to be passed here
# control: is (time_to_scen2 - time_from_scen2) = (time_to - time_from)
# otherwise the script will not work as intended     
# these variables will be ignored if the values are set to -1
time_from_scen2 = -1
time_to_scen2 = -1

if time_from_scen2 == -1:
    time_from_scen2 = time_from
if time_to_scen2 == -1:
    time_to_scen2 = time_to

# end of settings

# load selected files and folders 

# define the file and filepath for scenario 1
# as file_1, set the path selected in GUI for Data File 1
file_1 = datafile.value
# as scenario_1, choose the corresponding folder
scenario_1 = file_1[0:(len(file_1) - len(file_1.split("\\")[-1]))]

# define the file and filepath for scenario 2 (Data File 2 in GUI)
file_2 = datafile2.value
scenario_2 = file_2[0:(len(file_2) - len(file_2.split("\\")[-1]))]

# helper functions
identity = lambda x: x

# a=from, b=to, x=steps
def getDates(a, b, x):
    res = []
    for index in range(a, b+1, x):
        DataFile.SetEDXfileInSeries(EDXfileSeries, index)
        res.append(DataFile.associatedEDXFile.simdate)
    return res

# Main Script

# initialize - create empty arrays to store the data in the following (data1 for scenario1 and data2 for scenario2)
# we use numpy arrays (np) because they are much faster
data1 = np.empty([abs(time_to - time_from)+1, (abs(x_to - x_from)+1)*(abs(y_to - y_from)+1)*(abs(z_to - z_from)+1)], dtype = float)
data2 = np.empty([abs(time_to_scen2 - time_from_scen2)+1, (abs(x_to - x_from)+1)*(abs(y_to - y_from)+1)*(abs(z_to - z_from)+1)], dtype = float)
timesteps = []

# load EDX-file
# here we use implemented functions in the ENVI-met source code to directly access the data from the EDX-files 
# first, we need to read the EDX-file and -folder 
EDXfile.ReadFile(file_1)
EDXfileSeries.ReadFolder(scenario_1, EDXfile.SimBaseID)
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

# print variable names and units
for i in range(0, DataFile.GetLenOfNameVars()):
    print(str(i) + ': ' + DataFile.GetVarNameAndUnit(i))

# load data from scenario 1 and fill timesteps 
xTick_labels = []
for t in range(0, abs(time_to - time_from)+1):
    DataFile.SetEDXfileInSeries(EDXfileSeries, t + time_from)
    xTick_labels.append(DataFile.associatedEDXFile.simtime[0:2])
    timesteps.append(str(t))
    x = 0
    for i in range(0, abs(x_to - x_from)+1):
        for j in range(0, abs(y_to - y_from)+1):
            for k in range(0, abs(z_to - z_from)+1):
                data1[t][x] = DataFile.GetDataPointValue(data_index, i + x_from, j + y_from, k + z_from)
                x += 1


# load data from scenario 2
EDXfile.ReadFile(file_2)
EDXfileSeries.ReadFolder(scenario_2, EDXfile.SimBaseID)

for t in range(0, abs(time_to_scen2 - time_from_scen2)+1):
    DataFile.SetEDXfileInSeries(EDXfileSeries, t + time_from_scen2)
    x = 0
    for i in range(0, abs(x_to - x_from)+1):
        for j in range(0, abs(y_to - y_from)+1):
            for k in range(0, abs(z_to - z_from)+1):
                data2[t][x] = DataFile.GetDataPointValue(data_index, i + x_from, j + y_from, k + z_from)
                x += 1

# calculate the mean values for every timestep and save the values in vals1 and vals2
# these results are printed in the upper plot 
# alternatively we can calculate the max or min values for every timestep. To do so, just change the corresponding #-signs

#vals1 = (np.nanmin(data1, axis=1), "Min.")
#vals1 = (np.nanmax(data1, axis=1), "Max.")
vals1 = (np.nanmean(data1, axis=1), "Mean")

#vals2 = (np.nanmin(data2, axis=1), "Min.")
#vals2 = (np.nanmax(data2, axis=1), "Max.")
vals2 = (np.nanmean(data2, axis=1), "Mean")

# now we calculate the absolute difference for every timestep
# this is printed in the lower plot 
diff_vals = np.empty(vals1[0].size, dtype=float)
for i in range(0, diff_vals.size):
    diff_vals[i] = abs(vals1[0][i] - vals2[0][i])

# the data is now ready for the plot

# plot
if diagramtitle.value == '':
    dTitle = 'Comparison of ' + DataFile.GetVarNameAndUnit(data_index) + ' between Scenario A and B'
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
plots = [[],[]]
# now we add the plots iteratively  
count = 1
for i in plots:
    i.append(figure.add_subplot(ori + count))
    count += 1

# define first plot (direct comparison)
ax1 = plots[0][0]
# we would like to plot the mean values for both scenarios in the same graph.
# Hence, we call the plot-function two times, first with the mean values from scenario 1 and second with the mean values from scenario 2
ax1.plot(timesteps, vals1[0], color='green', label= vals1[1] + ' values Scenario A')
ax1.plot(timesteps, vals2[0], color='blue', label= vals2[1] + ' values Scenario B ')
# to visualize the gap, we fill the area between both graphs 
ax1.fill_between(timesteps, vals1[0], vals2[0], alpha=0.2)
# now we set the title of out first plot.
if startDate != endDate:
    ax1.set(xlabel='timesteps [h]', ylabel=DataFile.GetVarNameAndUnit(data_index), title= DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + endDate + ' ' + xTick_labels[-1] + ':00h)')
else:
    ax1.set(xlabel='timesteps [h]', ylabel=DataFile.GetVarNameAndUnit(data_index), title= DataFile.GetVarNameAndUnit(data_index) + ' (' + startDate + ' ' + xTick_labels[0] + ':00h - ' + xTick_labels[-1] + ':00h)')
# ... place the legend in the upper right corner 
ax1.legend(loc="upper right")
# ... add a grid to our plot
ax1.grid()
# set the labels for our x-axis (to show the timestep and not the file-index)
ax1.set_xticklabels(xTick_labels)
for label in ax1.xaxis.get_ticklabels()[1::2]:
    label.set_visible(False)
# now we define a secondary axis, where the date of the corresponding day is shown
secax = ax1.secondary_xaxis('top', functions=(identity, identity))
secax.set_xticklabels(getDates(time_from, time_to, 24))
# it is enough to show the date once every 24 hours, so we set setp = 24
secax.set_xticks(np.arange(time_from, time_to, step=24))
# To visualize that we plot multiple days, we add a vertical line every time the timestep is 00:00h
for i in range(len(xTick_labels)):
    if xTick_labels[i] == '00':
        ax1.axvline(x=timesteps[i])

# define second plot (absolute difference)
ax2 = plots[1][0]
# our second plot is a bar plot. Here we set the zorder = 3 to display the bars in the foreground
ax2.bar(timesteps, diff_vals, zorder=3)

# set the title for the second plot
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
figure.suptitle(dTitle)
figure.set_size_inches(20, 20)
plt.xticks(timesteps, xTick_labels)
plt.rcParams["figure.figsize"] = (75, 50)   
plt.subplots_adjust(left = 0.125, right = 0.9, bottom = 0.1, top = 0.9, wspace = 0.2, hspace = 0.3)
# show the result 
plt.show()
