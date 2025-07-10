import syre
import matplotlib.pyplot as plt

db = syre.Database()
assets = db.find_assets()
data_assets_before_fw = list(filter(lambda asset: asset.file.endswith("dark-before-eis-fw_2d.txt"), assets))
data_assets_before_rv = list(filter(lambda asset: asset.file.endswith("dark-before-eis-rv_2d.txt"), assets))
#data_assets_after_fw = list(filter(lambda asset: asset.file.endswith("dark-after-eis-fw_2d.txt"), assets))
#data_assets_after_rv = list(filter(lambda asset: asset.file.endswith("dark-after-eis-rv_2d.txt"), assets))
data_bf = data_assets_before_fw[0]
data_br = data_assets_before_rv[0]
#data_af = data_assets_after_fw[0]
#data_ar = data_assets_after_rv[0]

fig1,ax1 = plt.subplots()
ax1.set_box_aspect(1)

file_bf = open(data_bf.file, "r") 
i_mA_bf = []
V_V_bf = []

for line in file_bf:  
    if(line.startswith('#')):
        continue
    splitline = line.split('\t')
    i_mA_bf.append(abs(float(splitline[3])/0.00009))
    V_V_bf.append(float(splitline[2]))
file_bf.close()
    
file_br = open(data_br.file, "r") 
i_mA_br = []
V_V_br = []

for line in file_br:  
    if(line.startswith('#')):
        continue
    splitline = line.split('\t')
    i_mA_br.append(abs(float(splitline[3])/0.00009))
    V_V_br.append(float(splitline[2]))
file_br.close()

'''file_af = open(data_af.file, "r") 
i_mA_af = []
V_V_af = []

for line in file_af:  
    if(line.startswith('#')):
        continue
    splitline = line.split('\t')
    i_mA_af.append(abs(float(splitline[3])/0.00009))
    V_V_af.append(float(splitline[2]))
file_af.close()

file_ar = open(data_ar.file, "r") 
i_mA_ar = []
V_V_ar = []

for line in file_ar:  
    if(line.startswith('#')):
        continue
    splitline = line.split('\t')
    i_mA_ar.append(abs(float(splitline[3])/0.00009))
    V_V_ar.append(float(splitline[2]))
file_ar.close()'''



ax1.plot(V_V_bf, i_mA_bf, 'k--', alpha=0.6)
ax1.plot(V_V_br, i_mA_br, 'k-', alpha=0.6, label='Before EIS')
#ax1.plot(V_V_af, i_mA_af, 'b--')
#ax1.plot(V_V_ar, i_mA_ar, 'b-', label='After EIS')
ax1.set_ylim(0.001,50), 
ax1.set_xlim(0,1.2), 
ax1.set_xlabel('Voltage(V)') 
ax1.set_ylabel('Current Density (mA/cm2)')
ax1.set_yscale('log')
#ax1.vlines(0.0, -30,30, colors='k')
#ax1.hlines(0.0, -0.5,3, colors='k')
#ax1.set_ylim(4,-20), ax1.set_xlim(-0.1,1.0), ax1.set_xlabel('Voltage(V)'), ax1.set_ylabel('Current Density(mA/cm2)')
ax1.legend(loc='upper left')

fig_path = db.add_asset('darkIV.png')
fig1 = fig1.savefig(fig_path)
