def iV_SS(path, area):
    file = open(path,'r')
    v_V = []
    j_mA = []
    for line in file:  
        if(line.startswith('#')):
            continue
        splitline = line.split('\t')
        j_mA.append(float(splitline[3])/area)
        v_V.append(float(splitline[2]))
    file.close()
    return v_V, j_mA