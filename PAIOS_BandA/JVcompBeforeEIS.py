import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import syre

def iV_paios(path, area):
    file = open(path,'r')
    v_V = []
    i_mA = []
    for line in file:  
        if(line.startswith('#')):
            continue
        splitline = line.split('\t')
        i_mA.append(float(splitline[3])/area)
        v_V.append(float(splitline[2]))
    file.close()
    return v_V, i_mA

areas = [0.00009, 0.00016]
fig = plt.figure(figsize=(5,5))
ax1 = fig.gca()
ax1.set_xlim([-0.1,1.25])
ax1.set_ylim([2,-22])    
ax1.set_xlabel('Voltage (V)')
ax1.set_ylabel('Current Density (mA/cm2)')

fig2 = plt.figure(figsize = (5,5))
ax2 = fig2.gca()
ax2.set_xlim([-0.1,1.15])
ax2.set_ylim([2,-22])    
ax2.set_xlabel('Voltage (V)')
ax2.set_ylabel('Current Density (mA/cm2)')

df_before = pd.DataFrame(columns= ['X_rv','Y1_rv', 'Y2_rv','Y3_rv','Y4_rv','Y5_rv'])

db = syre.Database()
assets = db.find_assets()
jv_fws = list(filter(lambda asset: asset.file.endswith("light-before-eis-fw_2d.txt"), assets))
jv_rvs = list(filter(lambda asset: asset.file.endswith("light-before-eis-rv_2d.txt"), assets))

for device in jv_fws: 
    if device.metadata["sample"] == 'main':
        col = device.metadata['color']
        name = device.metadata['name']
        state = device.metadata['state']
        volt_fw, mA_fw = iV_paios(device.file,areas[1]) 
        alp = 0.2
        if state == 'after':
            if 'NC' in name:
                alp = 0.6
            ax2.plot(volt_fw, mA_fw, '--', color=col, alpha = alp)
        elif state == 'before':
            ax1.plot(volt_fw, mA_fw, '--', color=col, alpha = alp)

for device in jv_rvs: 
    if device.metadata["sample"] == 'main':
        col = device.metadata['color']
        name = device.metadata['name']
        state = device.metadata['state']   
        volt_rv, mA_rv = iV_paios(device.file,areas[1]) 
        alp = 0.5
        if state == 'after':
            if 'NC' in name:
                alp = 0.8
            ax2.plot(volt_rv, mA_rv, '-', color=col, alpha = alp, label=name+state)
        elif state == 'before':
            ax1.plot(volt_rv, mA_rv, '-', color=col, alpha = alp, label=name+state)


ax1.legend(loc='lower left')
ax2.legend(loc='lower left')
fig_path = db.add_asset('IVcompBefore-BeforeEIS.png')
fig = fig.savefig(fig_path)
fig_path2 = db.add_asset('IVcompAfter-BeforeEIS.png')
fig2 = fig2.savefig(fig_path2)