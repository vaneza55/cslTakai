import xml.etree.ElementTree as ET

parser = ET.XMLParser(encoding='ISO-8859-1')
meta = ET.parse('surface/New Simulation_FX_2021-08-06_10.00.00.EDX', parser=parser).getroot()

variable_names = meta.find('variables/name_variables').text.strip().split(',')
# print(variable_names)

nr_xdata = int(meta.find('datadescription/nr_xdata').text)
nr_ydata = int(meta.find('datadescription/nr_ydata').text)
nr_zdata = int(meta.find('datadescription/nr_zdata').text)

import numpy
data = numpy.fromfile('atmosphere/New Simulation_AT_2021-08-06_10.00.00.EDT','<f4')

cube = data.reshape((len(variable_names), nr_zdata, nr_ydata, nr_xdata))

t = numpy.array(cube[6,0,:,:])
t[0,0]=100
t[0,1]=100
print(t.shape)
print(nr_xdata)
import matplotlib.pyplot as plt
plt.imshow(t[:,:])
plt.ylim(0,nr_ydata-1)
plt.xlim(0,nr_xdata-1)
plt.show()
