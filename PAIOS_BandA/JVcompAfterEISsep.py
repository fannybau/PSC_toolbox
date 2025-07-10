import pandas as pd 
import matplotlib.pyplot as plt
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

fig = plt.figure(figsize = (5,5))
ax1 = fig.gca()
ax1.set_xlim([-0.1,1.15])
ax1.set_ylim([2,-22])    
ax1.set_xlabel('Voltage (V)')
ax1.set_ylabel('Current Density (mA/cm2)')

fig2 = plt.figure(figsize = (5,5))
ax2 = fig2.gca()
ax2.set_xlim([-0.1,1.15])
ax2.set_ylim([2,-22])    
ax2.set_xlabel('Voltage (V)')
ax2.set_ylabel('Current Density (mA/cm2)')


db = syre.Database()
assets = db.find_assets()
jv_rvs = list(filter(lambda asset: asset.file.endswith("light-after-eis-rv_2d.txt"), assets))
jv_fws = list(filter(lambda asset: asset.file.endswith("light-after-eis-fw_2d.txt"), assets))

for device in jv_fws: 
    if device.metadata["sample"] == 'main':
        col = device.metadata['color']
        name = device.metadata['name']
        state = device.metadata['state']
        volt, mA = iV_paios(device.file,areas[1]) 
        if state == 'after':
            if 'NC' in name:
                ax2.plot(volt, mA, '--', color=col, alpha = 0.4)
            else:
                ax1.plot(volt, mA, '--', color=col, alpha = 0.4)
        elif state == 'before':
            ax1.plot(volt, mA, '--', color=col, alpha = 0.3)
            ax2.plot(volt, mA, '--', color=col, alpha = 0.3)

for device in jv_rvs: 
    if device.metadata["sample"] == 'main':
        col = device.metadata['color']
        name = device.metadata['name']
        state = device.metadata['state']       
        volt, mA = iV_paios(device.file,areas[1]) 
        if state == 'after':
            if 'NC' in name:
                ax2.plot(volt, mA, '-', color=col, alpha = 0.8, label=name+state)
            else:
                ax1.plot(volt, mA, '-', color=col, alpha = 0.8, label=name+state)
        elif state == 'before':
            ax1.plot(volt, mA, '-', color=col, alpha = 0.5)
            ax2.plot(volt, mA, '-', color=col, alpha = 0.5)

ax1.legend(loc='lower left')
ax2.legend(loc='lower left')
fig_path = db.add_asset('IVcompC-AfterEIS.png')
fig = fig.savefig(fig_path)
fig_path2 = db.add_asset('IVcompNC-AfterEIS.png')
fig2 = fig2.savefig(fig_path2)