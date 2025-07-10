import pandas as pd
import numpy as np
import syre
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def linear_func(X, a, b):
    return a*X + b

def read_MS(path):
    column_names = []
    file = open(path, 'r')
    lines = file.readlines()
    i = 19 
    j = 0
    while i < 30: 
         column_names.append(lines[i].strip()[12:])
         i+=1
         j+=1
         print(column_names)
    file.close()
    df = pd.read_table(path, sep='\t', names=column_names,  skiprows=31) 
    freq = []
    capacitance = []
    V_V = []
    df['Capacitance (F)'] = -1 / (2 * np.pi * df['Sweep 1 - Frequency (Hz)'] * df[' Impedance Imag (Ohm)'])
    df['1/C^2 (F^-2)'] =  1/(df['Capacitance (F)']**2)
    # Calculate doping concentration (N_D) from the slope
    # N_D = 2 / (e * epsilon_0 * epsilon_r * slope)
    # Assuming epsilon_r (relative permittivity) = 11.9 for Si and epsilon_0 (permittivity of free space) = 8.854187817e-12 F/m
    return df

fig1 = plt.figure(figsize=(10, 6))
ax1 = fig1.gca()
ax1.set_box_aspect(1)
ax1.set_xlabel('Voltage (V)')
ax1.set_ylabel('1/C² (F^-2)')
ax1.set_ylim(-5E14,1.1E16)
ax1.set_title('Mott-Schottky Plot with Linear Fit')
ax1.grid(True)

epsilon_r = 11.9
epsilon_0 = 8.854187817e-12
e = 1.602176634e-19  # Elementary charge in C
start_voltage = 0
end_voltage = 1.1

V_fbs = []    #'Flat-band potential (V_fb): {V_fb:.2f} V'
N_dopings = []     #'Doping concentration (N_D): {N_D:.2e} cm^-3'


db = syre.Database()
assets = db.find_assets()
ms_files = list(filter(lambda asset: asset.file.endswith("c-v_1d.txt"), assets))

for device in ms_files: 
    if device.metadata["sample"] == 'main':
        col = device.metadata['color']
        #mark = device.metadata['marker']
        name = device.name
        df = read_MS(device.file)
        df_filtered = df[df['Sweep 1 - Frequency (Hz)']>=19000]
        ax1.scatter(df_filtered['Sweep 2 - Offset Voltage (V)'], df_filtered['1/C^2 (F^-2)'], c=col, alpha=0.8, s=2, label=name)
        start_lin = df_filtered['1/C^2 (F^-2)'].iloc[0]-df_filtered['1/C^2 (F^-2)'].iloc[0]/6
        end_lin = df_filtered['1/C^2 (F^-2)'].iloc[-1]+df_filtered['1/C^2 (F^-2)'].iloc[0]/8   #, df_filtered['1/C^2 (F^-2)'].iloc[-1]*12
        df_linear = df_filtered[(df_filtered['1/C^2 (F^-2)'] <= start_lin) & (df_filtered['1/C^2 (F^-2)'] >= end_lin)]
        ax1.plot(df_linear['Sweep 2 - Offset Voltage (V)'], df_linear['1/C^2 (F^-2)'], c=col, alpha=0.8)
        popt, pcov = curve_fit(linear_func, df_linear['Sweep 2 - Offset Voltage (V)'], df_linear['1/C^2 (F^-2)'], p0=[-start_lin, start_lin*10])
        a, b = popt
        V_fb = -b / a
        N_D = 2 / (e * epsilon_0 * epsilon_r * a)
        #V_fbs.append(V_fb)
        #N_dopings.append(N_D)
        ax1.plot(df_filtered['Sweep 2 - Offset Voltage (V)'], linear_func(df_filtered['Sweep 2 - Offset Voltage (V)'], *popt), color='k', alpha = 0.5)

#dopBandPot = pd.DataFrame({'Frequency (Hz)':df['Sweep 1 - Frequency (Hz)'].unique(),'Flat-band potentials (V_fb)':V_fbs, 'Doping concentration (N_D)': N_dopings}, columns = ['Frequency (Hz)','Flat-band potentials (V_fb)','Doping concentration (N_D)']) 
#meta_path = db.add_asset('MS_comparison.txt')
#print(dopBandPot)
#dopBandPot.to_csv(meta_path, index=True, sep='\t')
ax1.legend(loc='upper right', prop={'size': 7}, ncol=2)
fig_path = db.add_asset('Mott_Schottky_HF_comparison.png')
fig1 = fig1.savefig(fig_path)