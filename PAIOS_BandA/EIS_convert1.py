import pandas as pd    #Here the dataframe is sorted and columns get nicer names
import syre
import math 
import matplotlib.pyplot as plt

db = syre.Database()
assets = db.find_assets()
data_assets = list(filter(lambda asset: asset.file.endswith("66-is-at-different-light-at-voc_1d.txt"), assets))
datafile = data_assets[0]
column_names = []
file = open(datafile.file, 'r')
lines = file.readlines()
i = 20 
j = 0
while i < 31: 
    column_names.append(lines[i].strip()[12:])
    i+=1
    j+=1

df = pd.read_csv(datafile.file, sep='\t', names=column_names,  skiprows=32)  
#dataF = df[df['Sweep 1 - Offset Light Intensity (1)'] < 0.8]
desired_columns=['LightIntensity', 'Freq(Hz)', 'OffsetCurr(A)', 'Voc(V)', 'Time(s)', 'Zprime(Ohm)', 'Zbis(Ohm)', 'GD', 'X', 'Y']      
#now_named = ['Sweep 1 - Offset Light Intensity (1)', 'Sweep 2 - Frequency (Hz)', ' ()', 'Amplitude (Ohm)', 'Phase (rad)', 'Frequency (Hz)', 'Offset Voltage (V)', 'Offset Current (A)', 'Offset Light Intensity (1)',' Impedance Real (Ohm)', ' Impedance Imag (Ohm)']
now_named = column_names
dat = df[now_named]
LightPower = pd.DataFrame(columns = ['Voc(V)', 'LI', 'Estimated Power(mW/cm2)'])                   
#print(dat)
phase = [math.degrees(math.atan(-1*(zbi/zpi))) for zbi,zpi in zip(dat[' Impedance Imag (Ohm)'],dat[' Impedance Real (Ohm)'])]
data = pd.DataFrame({'LightIntensity': dat['Sweep 1 - Offset Light Intensity (1)'], 'Freq(Hz)': dat['Sweep 2 - Frequency (Hz)'], 'OffsetCurr(A)':dat['Offset Current (A)'], 'Voc(V)': dat['Offset Voltage (V)'], 'Time(s)': 0, 'Zprime(Ohm)':dat[' Impedance Real (Ohm)'] , 'Zbis(Ohm)': dat[' Impedance Imag (Ohm)'], 'GD':0, 'X':phase, 'Y':0}, columns = desired_columns)  


#Start = 0.01 #@@Here enter the starting Offset Voltage value
#End = 1  #@@Here enter the ending Offset Voltage value
Steps = 11  #@@Here enter number of Steps LI
#Step = (End-Start)/(Steps-1) 
#LI = [99.999997E-6, 372.75936E-6, 1.3894954E-3, 5.1794746E-3, 19.306978E-3, 71.968570E-3, 268.26957E-3, 1.0000000E+0]
#LI = [0.0000000E+0, 99.999997E-6, 372.99999E-6, 1.3900000E-3, 5.1799999E-3, 19.300001E-3, 71.999997E-3, 268.00001E-3, 829.99998E-3, 1.0000000E+0]
LI = [0.0000000E+0, 9.9999997E-6, 99.999997E-6, 372.99999E-6, 1.3900000E-3, 5.1799999E-3, 19.300001E-3, 71.999997E-3, 268.00001E-3, 829.99998E-3, 1.0000000E+0]

power = [0, 0.00001, 0.0006, 0.0219, 0.0856, 0.3281, 1.2750, 4.8563, 18.2500, 60.000, 67.5000]

i = 0
fig,axs = plt.subplots(ncols=2,nrows= 2, gridspec_kw={'width_ratios':[1,2],'height_ratios':[1.5,1.5]}) #add if you want to see Z'' and Z'
plt.subplots_adjust(wspace=0.5, hspace = 0.5)
ax1, ax2, ax4, ax5 = axs.flat
while i < Steps :
    light = LI[i]
    data_sep = data.loc[data['LightIntensity']== light]
    data_cut = data_sep.drop(columns='LightIntensity')
    Voc = (math.fsum(data_cut['Voc(V)'])/len(data_cut))
    LightPower.loc[i] = Voc, light, power[i]
    meta_path = db.add_asset('meta.txt')
    data_cut.to_csv(meta_path, index=True, sep='\t')
    data_cut_path = db.add_asset('temp/55-EIS1_'+str(round(light,5))+'_LI.txt')
    data_cut.to_csv(data_cut_path, index=False, sep='\t')  
    nf_path = db.add_asset('55-'+str(i)+'-'+str(round(light,5))+'LI_'+str(round(Voc, 2))+'Voc_Zview.txt')
    nf = open(nf_path, 'w')
    nf.write("""ZView Calculated Data File: Version 1.1
Raw Data
Sweep Frequency: Control Voltage
Date: 01-01-2021     "Time: 00:00:00
Zahner Zennium/IM6

c:\\data\\asonia\\converted files from PAIOS.txt
Frequency
0,2,0,1,4.00000E-01,2.00000E+06
82""")
    nf.write('\n')
    f2 = open(data_cut_path, 'r')
    nf.write(f2.read())
    nf.seek(0)
    #print(nf.read())
    nf.close()
    f2.close()
    i = i+1
    ax4.plot(data_cut['Zprime(Ohm)'], data_cut['Zbis(Ohm)'])
    ax1.plot(data_cut['Zprime(Ohm)'], data_cut['Zbis(Ohm)'])
    ax2.plot(data_cut['Freq(Hz)'], data_cut['X'])
    #ax3.plot(data_cut['Freq(Hz)'], data_cut['Zprime(Ohm)'])
    #ax6.plot(data_cut['Freq(Hz)'], -data_cut['Zbis(Ohm)'])
    ax1.autoscale(enable=False, axis='both', tight=True)
    ax4.autoscale(enable=False, axis='both', tight=True)
    ax5.autoscale(enable=False, axis='both', tight=True)
    #ax6.autoscale(enable=False, axis='both', tight=True)
    #ax6.plot(lipow['Estimated Power'], lipow['Voc'])
ax5.plot(LightPower['LI'], LightPower['Voc(V)'], 'ro')
ax1.set_ylim(1000,-30000), ax1.set_xlim(0,31000), ax1.set_xlabel('Zbis'), ax1.set_ylabel('Zprime'), ax1.legend()
ax2.set_xscale('log'), ax2.set_ylim(-20,100), ax2.set_xlabel('Frequency'), ax2.set_ylabel('theta(degrees)')
#ax3.set_xscale('log'), ax3.set_yscale('log'), ax3.set_xlabel('Frequency'), ax3.set_ylabel('Zprime')
ax4.set_ylim(5,-600), ax4.set_xlim(5,600), ax4.set_xlabel('Zbis'), ax4.set_ylabel('Zprime')
ax5.set_xscale('log'), ax5.set_ylim(0,1.15), ax5.set_xlim(0.000001,1.5), ax5.set_ylabel('Voc'), ax5.set_xlabel('Light Intensity')
#ax6.set_yscale('log'), ax6.set_xscale('log'), ax6.set_ylabel('-Zbis'), ax6.set_xlabel('Frequency'), ax6.set_ylim(0,1000000), ax6.set_xlim(0,1000000), 
#ax6.set_yscale('log'), ax6.set_xscale('log'), ax6.set_ylabel('Voc'), ax6.set_xlabel('Estimated input power')
fig_path = db.add_asset('55-EIS1.png')
fig = fig.savefig(fig_path)
meta_path = db.add_asset('meta.txt')
LightPower.to_csv(meta_path, index=True, sep='\t')