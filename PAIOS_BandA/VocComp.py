import pandas as pd 
import matplotlib.pyplot as plt
import syre

def meta_read(path):
    file = open(path, 'r')
    li = []
    voc = []
    i = 0
    for line in file:  
        if(i == 0):
            i+=1
            continue
        splitline = line.split('\t')
        li.append(float(splitline[1]))
        voc.append(float(splitline[3]))
    return li, voc

fig = plt.figure(figsize = (5,5))
ax1 = fig.gca()
ax1.set_yscale('log')
ax1.set_ylabel('Light Intensity (1/suns)')
ax1.set_xlabel('Voc (V)')
ax1.set_xlim(0, 1.15)
ax1.set_ylim(0.00008, 2)

db = syre.Database()
assets = db.find_assets()
li_voc = list(filter(lambda asset: asset.file.endswith("meta.txt"), assets))

for device in li_voc: 
    if device.metadata["sample"] == 'main':
        name = device.metadata['name']
        state = device.metadata['state']  
        col = device.metadata['color']
        li, voc = meta_read(device.file)
        alp = 0.2
        if state == 'after':
            alp=0.8
            if 'NC' in name:
                 alp = 0.5
            else:
                ax1.scatter(voc, li, c=col, alpha=alp, label=name+state)
        elif state == 'before':
            ax1.scatter(voc, li, c=col, alpha=0.2)
        ax1.plot(voc, li, c=col, alpha = 0.2)
 
ax1.legend(loc='upper left')
fig_path = db.add_asset('Voc_LI_comparison.png')
fig = fig.savefig(fig_path)