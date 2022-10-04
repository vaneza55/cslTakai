# 6時から12時の間で、東西と南北に走る２種類の道路の日射量とMRTの差と表面温度の差の平均をプロット
from tracemalloc import start
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import os

# 開始時刻と終了時刻
start_time = 6
end_time = 9

# 出力ファイルから各時間ごとの特定のデータを配列にして返す
def GenerateArray(foldername, property, hour):
    filename = os.path.join(foldername, property, hour+".EDX")
    parser = ET.XMLParser(encoding='ISO-8859-1')
    meta = ET.parse(filename, parser=parser).getroot()
    
    nr_xdata = int(meta.find('datadescription/nr_xdata').text)
    nr_ydata = int(meta.find('datadescription/nr_ydata').text)
    nr_zdata = int(meta.find('datadescription/nr_zdata').text)
    variable_names = meta.find('variables/name_variables').text.strip().split(',')   
    propertynum = {"atmosphere":10,"radiation":11,"surface":12}
    propertyheight = {"atmosphere":5,"radiation":0,"surface":0}
    
    filename = os.path.join(foldername, property, hour+".EDT")
    data = np.fromfile(filename,'<f4').reshape((len(variable_names), nr_zdata, nr_ydata, nr_xdata))
    
    return data[propertynum[property], propertyheight[property], :, :]

# データから東西と南北の道路での平均値を計算 
def CalculateMean(data):
    
    
if __name__ == '__main__':
    
    