#%%
import pandas as pd    
import syre
import math 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.ticker as mtick
#%%
def readEIS(fil, savePlot=False, zView=False, saveMeta=False):
    file = open(fil, "r") 
    #Start = 0.01 #@@Here enter the starting Offset Voltage value
    #End = 1  #@@Here enter the ending Offset Voltage value
    Steps = 9  #@@Here enter number of Steps
    #Step = (End-Start)/(Steps-1) 
    #LI = [99.999997E-6, 372.75936E-6, 1.3894954E-3, 5.1794746E-3, 19.306978E-3, 71.968570E-3, 268.26957E-3, 1.0000000E+0]
    LI = [99.999997E-6, 372.99999E-6, 1.3900000E-3, 5.1799999E-3, 19.300001E-3, 71.999997E-3, 268.00001E-3, 829.99998E-3, 1.0000000E+0]
    power = [0.0006, 0.0219, 0.0856, 0.3281, 1.2750, 4.8563, 18.2500, 60.000, 67.5000]

    LightIntensity = []
    FreqHz = []
    OffsetCurrA = [] 
    ZprimeOhm = []
    ZbisOhm = []
    Time = []
    GD = []
    X = []
    Y = []
    OFFVOLT = []
    #my_md = {}  #my_md = {"my_str": "hi", "my_num": 100} db.add_asset(<file>, metadata=my_md)

    for line in file:  
        if(line.startswith('#')):
            continue
        splitline = line.split('\t')
        LightIntensity.append(float(splitline[0]))
        FreqHz.append(float(splitline[3]))
        OffsetCurrA.append(float(splitline[5]))
        #TimeSec.append(float(splitline[7].strip()))
        ZprimeOhm.append(float(splitline[6]))
        ZbisOhm.append(float(splitline[7]))
        Time.append(0)
        GD.append(0)
        X.append(math.degrees(math.atan(-1*(float(splitline[7])/float(splitline[6])))))
        Y.append(0)
        OFFVOLT.append(float(splitline[4]))
        
    file.close()
    data = pd.DataFrame({'LightIntensity': LightIntensity, 'Freq(Hz)': FreqHz, 'OffsetCurr(A)':OffsetCurrA, 'Voc(V)': OFFVOLT, 'Time(s)':Time, 'Zprime(Ohm)':ZprimeOhm, 'Zbis(Ohm)':ZbisOhm, 'GD':GD, 'X':X, 'Y':Y}, columns=['LightIntensity', 'Freq(Hz)', 'OffsetCurr(A)', 'Voc(V)', 'Time(s)', 'Zprime(Ohm)', 'Zbis(Ohm)', 'GD', 'X', 'Y'])         
    LightPower = pd.DataFrame(columns = ['LI', 'Estimated Power(mW/cm2)', 'Voc(V)'])                   
    #print(data[0:5]) #Remove # if you want to see how the data looks before cutting(first 5 rows)
    #data.to_csv('ordered.txt', index=False) #This file is saved so you can have a look if something looks strange (it overwrites each new input)
    
    fig, axs = plt.subplots(ncols=2,nrows= 2, gridspec_kw={'width_ratios':[1,2],'height_ratios':[1.5,1.5]}) #add if you want to see Z'' and Z'
    plt.subplots_adjust(wspace=0.5, hspace = 0.4, right=0.97, top=0.97, left=0.17, bottom=0.17)
    ax1, ax2, ax4, ax5 = axs.flat
    ax1.set_ylim(50,-100050), ax1.set_xlim(0,100050), ax1.set_xlabel('Zbis (Ω)', fontsize=16), ax1.set_ylabel('Zprime (\u03A9)', fontsize=16)
    ax2.set_xscale('log'), ax2.set_ylim(-50,100), ax2.set_xlabel('Frequency (Hz)', fontsize=16), ax2.set_ylabel('theta (°)', fontsize=16)
    #ax3.set_xscale('log'), ax3.set_yscale('log'), ax3.set_xlabel('Frequency'), ax3.set_ylabel('Zprime')
    ax4.set_ylim(5,-300), ax4.set_xlim(5,300), ax4.set_xlabel('Zbis (Ω)', fontsize=16), ax4.set_ylabel('Zprime (\u03A9)', fontsize=16)
    ax5.set_xscale('log'), ax5.set_ylim(0.2,1.2), ax5.set_xlim(0.00005,1.5), ax5.set_ylabel('Voc (V)', fontsize=16), ax5.set_xlabel('Light Intensity (1 sun)', fontsize=16)
    #ax6.set_yscale('log'), ax6.set_xscale('log'), ax6.set_ylabel('-Zbis'), ax6.set_xlabel('Frequency'), ax6.set_ylim(0,1000000), ax6.set_xlim(0,1000000), 
    #ax6.set_yscale('log'), ax6.set_xscale('log'), ax6.set_ylabel('Voc'), ax6.set_xlabel('Estimated input power')
    ax1.autoscale(enable=False, axis='both', tight=True)
    ax4.autoscale(enable=False, axis='both', tight=True)
    ax5.autoscale(enable=False, axis='both', tight=True)
    ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f'{int(x/100000)}'))
    ax1.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f'{int(x/100000)}'))
    ax1.text(0.52, 0.98, 'x 10^5', transform=ax1.transAxes, va='top')
    ax4.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f'{int(x/100)}'))
    ax4.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f'{int(x/100)}'))
    ax4.text(0.52, 0.98, 'x 10^2', transform=ax4.transAxes, va='top')
    #ax1.tick_params(axis= 'both', style=mtick.FormatStrFormatter('%.0e'))
    #ax6.autoscale(enable=False, axis='both', tight=True)
    ax1.tick_params(axis='both', which='major', labelsize=12)
    ax2.tick_params(axis='both', which='major', labelsize=12)
    ax4.tick_params(axis='both', which='major', labelsize=12)
    ax5.tick_params(axis='both', which='major', labelsize=12)
    
    i = 0
    while i < Steps :
        light = LI[i]
        #print(light)
        separation_condition = data['LightIntensity'] == light
        data.loc[separation_condition, 'Step'] = int(i)
        data_cut = data[separation_condition].drop(columns=['LightIntensity','Step'])
        Voc = (math.fsum(data_cut['Voc(V)'])/len(data_cut))
        LightPower.loc[i] = light,power[i],Voc
        if zView == True:
            data_cut_path = db.add_asset('temp/55-EIS1_'+str(round(light,5))+'_LI.txt')
            data_cut.to_csv(data_cut_path, index=False, sep='\t')  
            nf_path = db.add_asset('55-'+str(i)+'-'+str(round(light,5))+'LI_'+str(round(Voc, 2))+'Voc_Zview.txt')
            nf = open(nf_path, 'w')
            nf.write('''ZView Calculated Data File: Version 1.1
            Raw Data
            Sweep Frequency: Control Voltage
            Date: 01-01-2021     "Time: 00:00:00
            Zahner Zennium/IM6
            
            c:\\data\\asonia\\converted files from PAIOS.txt
            Frequency
            0,2,0,1,4.00000E-01,2.00000E+06
            82''')
            nf.write('\n')
            f2 = open(data_cut_path, 'r')
            nf.write(f2.read())
            nf.seek(0)
            nf.close()
            f2.close()
        i = i+1
        ax5.plot(LightPower['LI'], LightPower['Voc(V)'], 'ro')
        ax4.plot(data_cut['Zprime(Ohm)'], data_cut['Zbis(Ohm)'])
        ax1.plot(data_cut['Zprime(Ohm)'], data_cut['Zbis(Ohm)'])
        ax2.plot(data_cut['Freq(Hz)'], data_cut['X'])
        #ax3.plot(data_cut['Freq(Hz)'], data_cut['Zprime(Ohm)'])
        #ax6.plot(data_cut['Freq(Hz)'], -data_cut['Zbis(Ohm)'])
        #ax6.plot(lipow['Estimated Power'], lipow['Voc'])

    if savePlot == True: 
        fig_path = db.add_asset('55-EIS1.png')
        fig = fig.savefig(fig_path)
    if saveMeta == True: 
        meta_path = db.add_asset('meta.txt')
        LightPower.to_csv(meta_path, index=True, sep='\t')
            
    return data, LightPower, fig
    
#%%

db = syre.Database()
assets = db.find_assets()
data_assets = list(filter(lambda asset: asset.file.endswith("55-is-at-different-light-at-voc_1d.txt"), assets))
dat = data_assets[0]
fil = dat.file
data, lipow, fig = readEIS(fil, True, True, False)
#%%
def gaussian(x, mean, amplitude, stddev): #Define a Gaussian function
    return amplitude * np.exp(-(x - mean)**2 / (2 * stddev**2))

def fit_peak(x, y):
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlabel('Log10 frequency')
    ax.set_ylabel('Theta = arctan(-Zbis/Zprime)')
    ax.plot(x,y)
    A_guess = max(y)
    mu_guess = x[np.argmax(y)]
    sigma_guess = 1
    try:
        popt, pcov = curve_fit(gaussian, x, y, maxfev=1000)
        ax.plot(x, gaussian(x, popt[0], popt[1], popt[2]), 'k--')
        mu = popt[0]
        A = popt[1]
        return mu, A, False  # Return peak position and success status
    except RuntimeError:
        ax.plot(x, gaussian(x, mu_guess, A_guess, sigma_guess), 'k--', alpha=0.5)
        return min(x), A_guess, True  # If fitting fails, return index of maximum value and failure status
        
#%% 
thetafit = pd.DataFrame(columns = ['LightIntensity', 'Voc', 'thetaLF_Center', 'thetaLF_Amplitude', 'DiscardFit'])

for step in data['Step'].unique():
    plot = data[data['Step']==step]
    #axi.plot(plot['Freq(Hz)'], plot['X'])
    low_frequency = plot[plot['Freq(Hz)'] < 10]
    x_data = low_frequency['Freq(Hz)'].to_numpy()
    logx_data = np.log10(x_data)
    y_data = low_frequency['X'].to_numpy()
    mean, Amp, bol = fit_peak(logx_data, y_data)
    print(np.exp(mean), Amp, bol)
    #axfit.plot(logx_data, gaussian(logx_data, popt[0], popt[1], popt[2]), 'k', style='--')
    new_instance = { # Data for the new row
        'LightIntensity': plot['LightIntensity'].iloc[0],
        'Voc': (math.fsum(plot['Voc(V)'])/len(plot)),
        'thetaLF_Center': np.exp(mean),  
        'thetaLF_Amplitude': Amp,
        'DiscardFit': bol
    }
    thetafit.loc[step] = new_instance
thetafit_path = db.add_asset('thetafit.txt')
thetafit.to_csv(thetafit_path, index=True, sep='\t')