import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import syre
import matplotlib.cm as cm

def iV_paios(path): #returns two arrays of voltage and current as read from PAIOS file
    file = open(path,'r')
    i_A = []
    v_V = []
    for line in file:
        if(line.startswith('#')):
            continue
        splitline = line.split('\t')
        i_A.append(float(splitline[3]))
        v_V.append(float(splitline[2]))
    file.close
    return v_V, i_A

def iVparam_paios(v_V, i_A):
    area = 0.16 #cm2 #Set for specific equipment
    irradiance = 0.83 #Set for specific equipment
    power_In = irradiance * (area*1e-4) #Set for specific equipment
    df = pd.DataFrame({'Voltage(V)':v_V, 'Current(A)':i_A}, columns=['Voltage(V)', 'Current(A)'])
    jsc = df.iloc[-6]['Current(A)']/(area*0.001)
    power = df['Current(A)']*df['Voltage(V)']*-1 
    pce = power.max()*0.001/(power_In)*100 #Percent, Efficiency = ((P_Max/1000)/(Power_In))*100
    list_vocs = df[df['Current(A)'] >= -0.0005]
    vocs = list_vocs.loc[list_vocs['Current(A)'] <= 0.0005]
    voc = vocs['Voltage(V)'].mean()
    ff = (power.max())/(jsc*voc*0.00016)*(-100) #((P_Max/1000)/(I_Short_Circuit*V_Open_Circuit))*(-100)
    i_mpp_A = df['Current(A)'][power.argmax()]
    v_mpp_V = df['Voltage(V)'][power.argmax()]
    return voc, jsc, pce, ff, power, v_mpp_V, i_mpp_A

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

def iv_SS(path):
    pce_ss = pd.read_excel(path, sheet_name='pce', index_col = "Sample")
    voc_ss = pd.read_excel(path, sheet_name='voc', index_col = "Sample") 
    ff_ss = pd.read_excel(path, sheet_name='ff', index_col = "Sample")
    jsc_ss = pd.read_excel(path, sheet_name='jsc', index_col = "Sample")
    return voc_ss, jsc_ss, pce_ss, ff_ss

def timeline_figure(sort):
    if sort == 'pce':
        fig = plt.figure(1,figsize = (10,6))
        pce_ax1 = plt.subplot(4,8,(1,2))
        pce_ax1.set_ylim(2,22)
        pce_ax1.set_ylabel('PCE (%)')
        #pce_ax1.set_xticklabels([])
        pce_ax2 = plt.subplot(4,8,(3,6))
        pce_ax2.set_ylim(2,22)
        pce_ax2.set_yticklabels([])
        #ax2a.set_xticklabels([])
        pce_ax3 = plt.subplot(4,8,(7,8))
        pce_ax3.set_ylim(2,22)
        pce_ax3.set_yticklabels([])
        #pce_ax3.set_xticklabels([])
        plt.subplots_adjust(wspace=0.03, hspace=0)
    return fig, pce_ax1, pce_ax2, pce_ax3

def pce_timeline(ax1, xB, yB, ax2, xS, yS, ax3, xA, yA, col, mark, colin):
    ax1.scatter(xB, yB, s=5, ec=col, marker=mark, fc = colin)
    ax2.plot(xS, yS,linewidth=0.5, color=col)
    dt = xS[1] - xS[0]
    color_change = 3*3600 #hours
    color_num = 10
    num_iterations = len(xS)
    cmap = cm.get_cmap('viridis', int(num_iterations/(color_change/dt))) 
    for i in range(len(xS)):
        c_points = int(i/(color_change/dt))
        colr = cmap(c_points)
        ax2.plot([xS[i], xS[i+1]], [15,20] , color = colr, linewith = 1)
    ax3.scatter(xA,yA, s=5, ec=col, marker=mark, fc = colin)
    return fig

def v_timeline(xB, yB, xS, yS, xA, yA, col, mark):
    if plt.fignum_exists(2) == 0:
        fig = plt.figure(2, figsize = (15,6))
    ax1b = plt.subplot(4,8,(9,11))
    ax1b.scatter(xB,yB, color=col, marker = mark)
    ax1b.set_ylim(0,1.2)
    ax1b.set_ylabel('Voc or Vmpp \n (V)')
    ax1b.set_xticklabels([])
    ax2b = plt.subplot(4,8,(12,13))
    ax2b.scatter(xS, yS, color=col, marker = mark)
    ax2b.set_ylim(0,1.2)
    ax2b.set_yticklabels([])
    ax2b.set_xticklabels([])
    ax3b = plt.subplot(4,8,(14,15))
    ax3b.scatter(xA,yA, color=col, marker = mark)
    ax3b.set_ylim(0,1.2)
    ax3b.set_yticklabels([])
    ax3b.set_xticklabels([])
    plt.subplots_adjust(wspace=0.03, hspace=0)
    plt.show()
    return fig

def i_timeline(xB, yB, xS, yS, xA, yA, col):
    if plt.fignum_exists(3) == 0:
        fig = plt.figure(3, figsize = (15,6))
        ax1c = plt.subplot(4,8,(17,19))
        ax1c.scatter(xB, yB, color=col)
        ax1c.set_ylim(0,24)
        ax1c.set_ylabel('Current Density \n (Jsc or Jmpp) -mA/cm2')
        ax2c = plt.subplot(4,8,(20,21))
        ax2c.scatter(xS, yS ,color=col)
        ax2c.set_ylim(0,24)
        ax2c.set_yticklabels([])
        ax3c = plt.subplot(4,8,(22,23))
        ax3c.scatter(xA,yA, color=col)
        ax3c.set_ylim(0,24)
        ax3c.set_yticklabels([])
        plt.subplots_adjust(wspace=0.03, hspace=0)
        plt.show()
        return fig
    
def decay(before, after):
    part_initial = (1-(after/before)) 
    return part_initial

# NOW HERE REPLICATING THE MAIN CALL USING SYRE SO THAT ALL SAMPLES CAN BE COMPARED Together
db = syre.Database()
ss_data = db.find_assets(type ='collectiveIV')[0]
voc_ss, jsc_ss, pce_ss, ff_ss = iv_SS(ss_data.file)
fig, ax1, ax2, ax3 = timeline_figure('pce')
index = ['Device', 'variation']
x_before = ['SS1','SS2','bbEIS','baEIS','bS']
x_after = ['aS','abEIS','aaEIS','SS3']
df_pce = pd.DataFrame(columns=index+x_before+x_after)
for variation in #children: 
    devices = variation.#children()
    for device in devices: 
        if device.metadata["sample"] == 'main':
            assets = device.assets
            lb = list(filter(lambda asset: asset.file.endswith("0_0_Perform parallel JV.csv"), assets))[0]
            la = list(filter(lambda asset: asset.file.endswith("2_0_Perform parallel JV.csv"), assets))[0]
            lb_voc, lb_jsc, lb_pce, lb_ff, lb_power, lb_vmpp, lb_jmpp, lb_rv, lb_fw = iV_litos(lb.file)
            la_voc, la_jsc, la_pce, la_ff, la_power, la_vmpp, la_jmpp, la_rv, la_fw = iV_litos(la.file)
            stressing = list(filter(lambda asset: asset.file.endswith("1_0_Stressing.csv"), assets))[0]
            stress = stress_litos(stressing.file)
            instances = device.#children()
            for instance in instances: 
                if instance.metadata['LOGG'] == 'before':
                    #print(instance.metadata)
                    assets = instance.assets
                    bbEIS = list(filter(lambda asset: asset.file.endswith('44-jv-light-before-eis-rv_2d.txt'), assets))[0]
                    baEIS = list(filter(lambda asset: asset.file.endswith('77-jv-light-after-eis-rv_2d.txt'), assets))[0]
                    vbbEIS, ibbEIS = iV_paios(bbEIS.file)
                    vbaEIS, ibaEIS = iV_paios(baEIS.file)
                    voc_bbEIS, jsc_bbEIS, pce_bbEIS, ff_bbEIS, power_bbEIS, v_mpp_V_bbEIS, i_mpp_A_bbEIS = iVparam_paios(vbbEIS, ibbEIS)
                    voc_baEIS, jsc_baEIS, pce_baEIS, ff_baEIS, power_baEIS, v_mpp_V_baEIS, i_mpp_A_baEIS = iVparam_paios(vbaEIS, ibaEIS)

                if instance.metadata['LOGG'] == 'after':
                    #print(instance.metadata)
                    assets = instance.assets
                    abEIS = list(filter(lambda asset: asset.file.endswith('44-jv-light-before-eis-rv_2d.txt'), assets))[0]
                    aaEIS = list(filter(lambda asset: asset.file.endswith('77-jv-light-after-eis-rv_2d.txt'), assets))[0]
                    vabEIS, iabEIS = iV_paios(abEIS.file)
                    vaaEIS, iaaEIS = iV_paios(aaEIS.file)
                    voc_abEIS, jsc_abEIS, pce_abEIS, ff_abEIS, power_abEIS, v_mpp_V_abEIS, i_mpp_A_abEIS = iVparam_paios(vabEIS, iabEIS)
                    voc_aaEIS, jsc_aaEIS, pce_aaEIS, ff_aaEIS, power_aaEIS, v_mpp_V_aaEIS, i_mpp_A_aaEIS = iVparam_paios(vaaEIS, iaaEIS)
            if device.metadata['variation'] == 'Ref':
                pce_ss1 = pce_ss[device.name:device.name]['20231012-all'][1]
                pce_ss2 = pce_ss[device.name:device.name]['20231016-all'][1]
                pce_ss3 = pce_ss[device.name:device.name]['20231017 - ref'][0]
                pce_y_before = [pce_ss1, pce_ss2, pce_bbEIS, pce_baEIS, lb_pce]
                pce_y_after = [la_pce, pce_abEIS, pce_aaEIS, pce_ss3]
                x_stress = stress['#time (s)']/3600
                pce_y_stress = stress['PCE (%)']
                pce_timeline(ax1, x_before, pce_y_before, ax2, x_stress, pce_y_stress, ax3, x_after, pce_y_after, 'yellowgreen', 's','yellowgreen')
            if device.metadata['variation'] == 'Mod':
                pce_ss1 = pce_ss[device.name:device.name]['20231012-all'][1]
                pce_ss2 = pce_ss[device.name:device.name]['20231016-all'][1]
                pce_ss3 = pce_ss[device.name:device.name]['20231018-mod'][0]
                pce_y_before = [pce_ss1, pce_ss2, pce_bbEIS, pce_baEIS, lb_pce]
                pce_y_after = [la_pce, pce_abEIS, pce_aaEIS, pce_ss3]
                x_stress = stress['#time (s)']/3600
                pce_y_stress = stress['PCE (%)']
                pce_timeline(ax1, x_before, pce_y_before, ax2, x_stress, pce_y_stress, ax3, x_after, pce_y_after, 'crimson', 'o', 'w')
            df_pce.loc[len(df_pce.index)] = [device.name, device.metadata['variation'],pce_ss1,pce_ss2, pce_bbEIS, pce_baEIS, lb_pce, la_pce, pce_abEIS, pce_aaEIS, pce_ss3]
pce_table_path = db.add_asset('Main_PCE_for_stats.txt')
df_pce.to_csv(pce_table_path, index=False, sep='\t')  #@@Here enter file reference. Program also adds a reference to the file-name and saves a new file each voltage
fig_path = db.add_asset('pce_timeline.png')
fig = fig.savefig(fig_path)

