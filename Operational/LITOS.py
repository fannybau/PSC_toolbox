import syre
import matplotlib.pyplot as plt
import pandas as pd

db = syre.Database()
assets = db.find_assets()
data_assets_Stress = list(filter(lambda asset: asset.file.endswith("0_Stressing.csv"), assets))
data_assets_JV_before = list(filter(lambda asset: asset.file.endswith("0_0_Perform parallel JV.csv"), assets))
data_assets_JV_after = list(filter(lambda asset: asset.file.endswith("2_0_Perform parallel JV.csv"), assets))
data1 = data_assets_Stress[0].file
data2 = data_assets_JV_before[0].file
data3 = data_assets_JV_after[0].file

iV_before = pd.read_table(data2, delimiter=',', skiprows=17, encoding='latin_1')
iV_after = pd.read_table(data3, delimiter=',', skiprows=17, encoding='latin_1')
stressing = pd.read_table(data1, delimiter=',', skiprows=20, encoding='latin_1')


rows1 = len(iV_before.index)
rows2 = len(iV_before.index)
split1 = int(rows1/2)
split2 = int(rows2/2)
iVbefore_fw = iV_before.iloc[split1:,:]
iVbefore_rv = iV_before.iloc[:split1,:]
iVafter_fw = iV_after.iloc[split2:,:]
iVafter_rv = iV_after.iloc[:split2,:]

area = 0.16
power_in = 1
power = (stressing['Current (mA)']*stressing['Voltage (V)'])
pce = power/(area*power_in)
stressing.insert(3,'PCE (%)',pce)
pce_max = stressing['PCE (%)'].max()
pce_max_index = stressing['PCE (%)'].idxmax()
stressing.insert(4,'PCE_normalized[1,0]', stressing['PCE (%)']/pce_max)


'''fig = plt.figure()
ax1 = plt.subplot(3,2,1)
ax1.set_box_aspect(1)
ax1.plot(iVbefore_fw['#voltage (V)'], iVbefore_fw['current (mA)'], 'g--')
ax1.plot(iVbefore_rv['#voltage (V)'], iVbefore_rv['current (mA)'], 'g-')
ax1.plot(iVafter_fw['#voltage (V)'], iVafter_fw['current (mA)'], 'r--')
ax1.plot(iVafter_rv['#voltage (V)'], iVafter_rv['current (mA)'], 'r-')
ax2 = plt.subplot(3,2,2)
ax2.plot(stressing['#time (s)']/3600, stressing['Current (mA)'], 'y-')
ax3 = ax2.twinx()
ax3.plot(stressing['#time (s)']/3600, stressing['Voltage (V)'], 'm-')
ax4 = plt.subplot(3,1,2)
ax4.plot(stressing['#time (s)']/3600, (stressing['Current (mA)']*stressing['Voltage (V)'])/0.16, 'k-')
ax1.set_ylim(-0.5,3), ax1.set_xlim(-0.1,1.1), ax1.set_xlabel('Voltage(V)'), ax1.set_ylabel('Current(mA)')
ax2.set_xlabel('Time (h)'), ax2.set_ylabel('Current(mA)')
ax3.set_ylabel('Voltage (V)')
ax4.set_xlabel('Time (h)'), ax4.set_ylabel('~PCE(%)')
plt.subplots_adjust(wspace=0.2, hspace = 1)
fig_path = db.add_asset('LITOS.png')
fig = fig.savefig(fig_path)'''

before_jsc = iVbefore_rv.iloc[-6]/area
before_power = iVbefore_rv['current (mA)']*iVbefore_rv['#voltage (V)']
before_pce = before_power.max()/area
after_jsc = iVafter_rv.iloc[-6]/area
after_power = iVafter_rv['current (mA)']*iVafter_rv['#voltage (V)']
after_pce = after_power.max()/area
test_s = stressing['#time (s)'].max()
fig2 = plt.figure()
ax_1 = plt.subplot(211)
ax_1.scatter(stressing['#time (s)']/3600, stressing['PCE (%)'])
ax_1.scatter([0,test_s/3600],[before_pce, after_pce])
ax_1.set_ylabel('PCE(%)')
ax_2 = plt.subplot(212)
ax_2.scatter(stressing['#time (s)']/3600, stressing['Current (mA)']/area)
ax_2.scatter([0,test_s/3600],[before_jsc[1], after_jsc[1]])
ax_2.set_ylabel('Current(mA)')
ax_2.set_xlabel('Time(h)')
fig2_path = db.add_asset('stressing.png')
fig2.savefig(fig2_path)
pce_path = db.add_asset('stressing.csv')
stressing.to_csv(pce_path,index=False, sep='\t')