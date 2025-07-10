import syre
import matplotlib.pyplot as plt

db = syre.Database()
assets = db.find_assets()
data_assets_before_fw = list(filter(lambda asset: asset.file.endswith("light-before-eis-fw_2d.txt"), assets))
data_assets_before_rv = list(filter(lambda asset: asset.file.endswith("light-before-eis-rv_2d.txt"), assets))
data_assets_after_fw = list(filter(lambda asset: asset.file.endswith("light-after-eis-fw_2d.txt"), assets))
data_assets_after_rv = list(filter(lambda asset: asset.file.endswith("light-after-eis-rv_2d.txt"), assets))
data1 = data_assets_before_fw[0]
data2 = data_assets_before_rv[0]
data3 = data_assets_after_fw[0]
data4 = data_assets_after_rv[0]

fig,ax1 = plt.subplots()
ax1.set_box_aspect(1)

file1 = open(data1.file, "r") 
i_mA1 = []
V_V1 = []

for line in file1:  
    if(line.startswith('#')):
        continue
    splitline = line.split('\t')
    i_mA1.append(float(splitline[3])/0.00016)
    V_V1.append(float(splitline[2]))
file1.close()
    
file2 = open(data2.file, "r") 
i_mA2 = []
V_V2 = []

for line in file2:  
    if(line.startswith('#')):
        continue
    splitline = line.split('\t')
    i_mA2.append(float(splitline[3])/0.00016)
    V_V2.append(float(splitline[2]))
file2.close()

file3 = open(data3.file, "r") 
i_mA3 = []
V_V3 = []

for line in file3:  
    if(line.startswith('#')):
        continue
    splitline = line.split('\t')
    i_mA3.append(float(splitline[3])/0.00016)
    V_V3.append(float(splitline[2]))
file3.close()

file4 = open(data4.file, "r") 
i_mA4 = []
V_V4 = []

for line in file4:  
    if(line.startswith('#')):
        continue
    splitline = line.split('\t')
    i_mA4.append(float(splitline[3])/0.00016)
    V_V4.append(float(splitline[2]))
file4.close()


ax1.plot(V_V1, i_mA1, 'g--')
ax1.plot(V_V2, i_mA2, 'g-')
ax1.plot(V_V3, i_mA3, 'k--')
ax1.plot(V_V4, i_mA4, 'k-')
ax1.set_ylim(2,-22), ax1.set_xlim(-0.1,1.1), ax1.set_xlabel('Voltage(V)'), ax1.set_ylabel('Current(mA/cm2)')

fig_path = db.add_asset('IV.png')
fig = fig.savefig(fig_path)