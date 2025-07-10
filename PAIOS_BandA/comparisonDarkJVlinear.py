import syre
import matplotlib.pyplot as plt


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

figbefore = plt.figure(figsize = (5,5))
ax1 = figbefore.gca()
ax1.set_ylim(-0.1,16), 
ax1.set_xlim(0.1,1.10), 
ax1.set_xlabel('Voltage(V)'), ax1.set_ylabel('Current Density (mA/cm2)')

figafter = plt.figure(figsize = (5,5))
ax2 = figafter.gca()
ax2.set_ylim(-0.1,16), 
ax2.set_xlim(0.1,1.10),  
ax2.set_xlabel('Voltage(V)'), ax2.set_ylabel('Current Density (mA/cm2)')

db = syre.Database()
assets = db.find_assets()
dark_fws = list(filter(lambda asset: asset.file.endswith("8-jv-dark-before-eis-fw_2d.txt"), assets))
dark_rvs = list(filter(lambda asset: asset.file.endswith("9-jv-dark-before-eis-rv_2d.txt"), assets))

for device in dark_fws: 
    if device.metadata["sample"] == 'main':
        col = device.metadata['color']
        name = device.metadata['name']
        state = device.metadata['state']
        volt_bf, mA_bf = iV_paios(device.file,areas[1]) 
        if state == 'after': 
            if 'N' in name:
                col = 'g'
            ax2.plot(volt_bf, mA_bf, '--', color = col, alpha = 0.2)
        elif state == 'before': 
            ax2.plot(volt_bf, mA_bf, '--', color = col, alpha = 0.2)
        
for device in dark_fws: 
    if device.metadata["sample"] == 'main':
        col = device.metadata['color']
        name = device.metadata['name']
        state = device.metadata['state']
        volt_br, mA_br = iV_paios(device.file,areas[1]) 
        alp = 0.4
        if state == 'after':
            if 'N' in name:
                alp = 0.8   
            ax2.plot(volt_br, mA_br, '-', color = col, alpha = alp, label=name+state)
        elif state == 'before':    
            ax2.plot(volt_br, mA_br, '-', color = col, alpha = 0.6, label=name+state)
        
ax1.legend(loc='upper left')
ax2.legend(loc='upper left')
fig_path1 = db.add_asset('darkIV_before_linear.png')
figbefore = figbefore.savefig(fig_path1)
fig_path2 = db.add_asset('darkIV_after_linear.png')
figafter = figafter.savefig(fig_path2)
