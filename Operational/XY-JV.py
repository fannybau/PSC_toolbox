import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import syre
import matplotlib.cm as cm

def iV_litos(path):
    iv = pd.read_table(path, delimiter=',', skiprows=17, encoding='latin_1') #specific for measurment
    rows = len(iv.index)
    split = int(rows/2)
    fw = iv.iloc[split:,:]
    rv = iv.iloc[:split,:]
    area = 0.16 #set to holder area
    jsc = rv.iloc[-6][1]/area  #this will need to be changed in a future version, maybe use numpy instead create df in the end
    power = rv['current (mA)']*rv['#voltage (V)']
    jmpp = rv['current (mA)'][power.idxmax()]
    vmpp = rv['#voltage (V)'][power.idxmax()]
    pce = power.max()/area
    list_vocs = rv[rv['current (mA)'] <= 1]
    vocs = list_vocs[list_vocs['current (mA)'] >= -1]
    voc = vocs['#voltage (V)'].mean()
    ff = (power.max())/(jsc*voc*0.00016)*(-100)
    return voc, jsc, pce, ff, power, vmpp, jmpp, rv, fw
    
def stress_litos(path):
    stress = pd.read_table(path, delimiter=',', skiprows=20, encoding='latin_1')
    area = 0.16  #set to holder area
    power = (stress['Current (mA)']*stress['Voltage (V)'])
    pce = power/area
    stress.insert(3,'PCE (%)',pce)
    pce_max = stress['PCE (%)'].max()
    pce_max_index = stress['PCE (%)'].idxmax()
    stress.insert(4,'PCE_normalized[1,0]', stress['PCE (%)']/pce_max)
    return stress


db = syre.Database()
assets = db.find_assets()
lb = list(filter(lambda asset: asset.file.endswith("0_0_Perform parallel JV.csv"), assets))[0]
la = list(filter(lambda asset: asset.file.endswith("2_0_Perform parallel JV.csv"), assets))[0]
stressing = list(filter(lambda asset: asset.file.endswith("1_0_Stressing.csv"), assets))[0]

df_stress = stress_litos(stressing.file)
fig = plt.figure(figsize=(5,5))
ax1 = plt.gca()
max1 = 10
dt = df_stress['#time (s)'].iloc[1] - df_stress['#time (s)'].iloc[0]
color_change = 3*3600 #hours
color_num = 10
num_iterations = len(df_stress.index)
cmap = cm.get_cmap('viridis', int(num_iterations/(color_change/dt)))  #matplotlib.colormaps.get_cmap('viridis') 
voc, jsc, pce, ff, power, vmpp, jmpp, df_rv, df_fw  = iV_litos(lb.file)
colb = cmap(0)
ax1.scatter(vmpp,jmpp/0.16, color = colb,  marker = 's', linewidths = 0.2, s = 20)
if assets[0].metadata['var'] == 'Mod':
    colarray = ['red', 'orangered']
if assets[0].metadata['var'] == 'Ref':
    colarray = ['navy', 'steelblue',]
ax1.plot([],[], color = colarray[0], alpha = 0.9, linewidth = 2, label = 'Before rv')
ax1.plot([],[], color = colarray[1], alpha = 0.6, linewidth = 2, label = 'After rv')
ax1.plot([],[], color = 'k',linestyle='--', alpha = 0.5, linewidth = 2, label = 'fw' )

ax1.plot(df_rv['#voltage (V)'],df_rv['current (mA)']/0.16, colarray[0], alpha = 0.9, linewidth = 2)
ax1.plot(df_fw['#voltage (V)'],df_fw['current (mA)']/0.16, colarray[0], linestyle='--', alpha = 0.9, linewidth = 2)
ax1.set_ylabel('Current Density (mA/cm2)', fontsize=12)
ax1.set_xlabel('Voltage (V)', fontsize=12)
ax1.tick_params(axis='both', which='major', labelsize=12)
ax1.axhline(y=0, linewidth=2, color = 'k', alpha = 0.2)
ax1.axvline(x=0, linewidth=2, color = 'k', alpha = 0.2)  #xmin=0.25, xmax=0.402, 
c_point = 0
fig2 = plt.figure(figsize=(2,4))
ax2 =fig2.gca()
for i in range(num_iterations):
    c_points = int(i/(color_change/dt))
    colr = cmap(c_points)
    ax2.plot([0,1], [i, i+1] , color = colr)

max = max1
max2 = max1*10 #includes less points beyond a threshold
skip = max
points = 0
for i in range(len(df_stress.index)):
    if skip<max:
        skip +=1
    else:
        skip = 0
        c_points = int(i/(color_change/dt))
        colr = cmap(c_points)
        #hours = int(i/(color_change/dt))
        if c_points > 3:
            max = max2
        #elif hours < 20:
        #    c_point = c_point + int(i/(8*color_change/dt))
        #else: 
        #    c_point = color_num
        #colr = cmap(c_point)
        ax1.scatter(df_stress['Voltage (V)'].iloc[i], df_stress['Current (mA)'].iloc[i]/0.16, color = colr, s = 2)

avoc, ajsc, apce, aff, apower, avmpp, ajmpp, adf_rv, adf_fw  = iV_litos(la.file)
cola = cmap(c_points)
ax1.scatter(avmpp,ajmpp/0.16, color = cola, marker = 's', linewidths = 0.2, s = 20)
ax1.plot(adf_rv['#voltage (V)'],adf_rv['current (mA)']/0.16, color=colarray[1], alpha = 0.6, linewidth = 2)
ax1.plot(adf_fw['#voltage (V)'],adf_fw['current (mA)']/0.16, color=colarray[1], linestyle='--', alpha = 0.6, linewidth = 2)
ax1.set_xlim(-0.1, 1.1)
ax1.set_ylim(-2, 18)
ax1.legend(loc='lower center', bbox_to_anchor=(0.5, 0.1), frameon=False, fontsize=12)

meta_path = db.add_asset('litosXY_JV.txt')
meta_file = open(meta_path, 'w')
meta_file.write('Time between showed points: ' + str(dt*max1) + ' seconds, first 6 hours')
meta_file.write('Time between showed points: ' + str(dt*max2) + ' seconds, after 6 hours')
meta_file.write('Colour change every ' + str(color_change/3600) + ' hours')
meta_file.write('Total time: ' + str(df_stress['#time (s)'].iloc[-1]/3600) + ' hours')
#print('Colour change every ' + str(8*color_change/3600) + ' hours, 6-20 hours')
#print('Beyond 20 hours, no change')

fig_path = db.add_asset('litosXY_JV.png')
fig = fig.savefig(fig_path)
fig_path2 = db.add_asset('litos_colorLegend.png')
fig2 = fig2.savefig(fig_path2)