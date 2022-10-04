# 6時から12時の間で、東西と南北に走る２種類の道路の日射量とMRTの差と表面温度の差の平均をプロット
from tracemalloc import start
import numpy as np
import xml.etree.ElementTree as ET
import os


# 出力ファイルからデータを配列にして返す
# 二次元配列だが、配列の添え字とxyが逆に注意
def GenerateArray(foldername, property, hour):
    filename = os.path.join(foldername, property, hour+".EDX")
    parser = ET.XMLParser(encoding='ISO-8859-1')
    meta = ET.parse(filename, parser=parser).getroot()
    
    nr_xdata = int(meta.find('datadescription/nr_xdata').text)
    nr_ydata = int(meta.find('datadescription/nr_ydata').text)
    nr_zdata = int(meta.find('datadescription/nr_zdata').text)
    variable_names = meta.find('variables/name_variables').text.strip().split(',')   
    propertynum = {"atmosphere":26,"radiation":18,"surface":6}
    propertyheight = {"atmosphere":5,"radiation":0,"surface":0}
    
    filename = os.path.join(foldername, property, hour+".EDT")
    data = np.fromfile(filename,'<f4').reshape((len(variable_names), nr_zdata, nr_ydata, nr_xdata))
    print(variable_names[propertynum[property]])
    return data[propertynum[property], propertyheight[property], :, :]

# データから東西と南北の道路での平均値を計算 
def CalculateMean(data):
    north = [42,182,106,186]
    south = [42,49,106,53]
    east = [106,53,111,182]
    west = [37,53,42,182]
    
    mean = []
    for dir in [north,south,east,west]:
        tmp = 0
        for y in range(dir[1], dir[3]):
            for x in range(dir[0], dir[2]):
                tmp += data[y][x]/((dir[2]-dir[0])*(dir[3]-dir[1]))
        mean.append(tmp)
    return [(mean[0]+mean[1])*0.5, (mean[2]+mean[3])*0.5]
    
if __name__ == '__main__':
    # 開始時刻と終了時刻
    start_time = 6
    end_time = 9
    
    data = GenerateArray("Asphalt", "atmosphere", "6")
    print(CalculateMean(data))
    