import numpy as np
import matplotlib.pyplot as plt
cmap = plt.cm.get_cmap("Reds", 10)

ystart, xstart, yend, xend, ysize, xsize = -0.5, -0.5, 0, 0.5, 501, 1001
scaling = (28e9*np.pi)/(2*np.pi)/9.5e10
kappa = 50e3
gamma = 10e6
loc_g0 = 'C:\\Users\\avillanueva\\Documents\\resonator-design\\data_files\\80nm_double.txt'
loc_implantation = 'C:\\Users\\avillanueva\\Documents\\resonator-design\\data_files\\implantation_profiles\\20keV.txt'

def read_g0(location):
    file_data = np.genfromtxt(location, usecols=(0,1,2,3,4), skip_header=9, dtype=float)
    g0 = np.reshape(file_data[:,4], (ysize, xsize))*scaling
    return g0

def plot_g0(location):
    g0 = read_g0(location)
    x = np.linspace(xstart,xend,xsize)
    y = np.linspace(ystart,yend,ysize)
    c = plt.pcolormesh(x,y,g0,shading='nearest',cmap=cmap)#vmin=3e-8,vmax=-3e-8)
    plt.colorbar(c, label='$g_0$/2$\pi$ (Hz)')
    plt.xlabel('x ($\mu$m)')
    plt.ylabel('y ($\mu$m)')
    plt.show()

def read_implantation(location):
    profile = np.genfromtxt(location, usecols=(0,1), skip_header=0, dtype=float)
    depth = profile[:,0]*1e-10*1e9
    concentration = profile[:,1]/(1e15)
    return depth, concentration

def plot_gens(location, loc_implantation):
    depth, concentration = read_implantation(loc_implantation)
    g0 = read_g0(location)
    x = np.linspace(xstart,xend,xsize)
    y = np.linspace(ystart,yend,ysize)
    y_rev = np.flip(y)
    sum_depth_slice = []
    for i in range(len(g0[:,0])):
        sum_depth_slice.append(sum(g0[i,:]))
    sum_depth_slice_rev = np.flip(sum_depth_slice)
    #plt.plot(range(len(g0[:,i])), sum_depth_slice_rev)
    #plt.show()
    g_ens = sum_depth_slice_rev[0:len(concentration)]*sum_depth_slice_rev[0:len(concentration)]*concentration
    plt.plot(y_rev[0:len(concentration)], g_ens)
    plt.xlabel('Depth (nm)')
    plt.ylabel('$g_{ens}^2/4\pi$ (Hz$^2$/nm)')
    plt.show()
    return g_ens

def cooperativity(location, loc_implantation, kappa, gamma):
    depth, concentration = read_implantation(loc_implantation)
    g0 = read_g0(location)
    x = np.linspace(xstart,xend,xsize)
    y = np.linspace(ystart,yend,ysize)
    y_rev = np.flip(y)
    sum_depth_slice = []
    for i in range(len(g0[:,0])):
        sum_depth_slice.append(sum(g0[i,:]))
    sum_depth_slice_rev = np.flip(sum_depth_slice)
    g_ens = sum_depth_slice_rev[0:len(concentration)]*sum_depth_slice_rev[0:len(concentration)]*concentration
    C = 4*sum(g_ens)/(kappa*gamma)
    print('Cooperativity is', C)
    return C

def plot_profiles():
    depth20, concentration20 = read_implantation('C:\\Users\\avillanueva\\Documents\\resonator-design\\data_files\\implantation_profiles\\20keV.txt')
    depth90, concentration90 = read_implantation('C:\\Users\\avillanueva\\Documents\\resonator-design\\data_files\\implantation_profiles\\90keV.txt')
    depth220, concentration220 = read_implantation('C:\\Users\\avillanueva\\Documents\\resonator-design\\data_files\\implantation_profiles\\220keV.txt')
    depth470, concentration470 = read_implantation('C:\\Users\\avillanueva\\Documents\\resonator-design\\data_files\\implantation_profiles\\470keV.txt')

    plt.plot(depth20, concentration20, label='20 keV')
    plt.plot(depth90, concentration90, label='90 keV')
    plt.plot(depth220, concentration220, label='220 keV')
    plt.plot(depth470, concentration470, label='470 keV')

    plt.xlabel('Depth (nm)')
    plt.ylabel('Concentration (nm$^{-1}$)')

    plt.show()

plot_g0(loc_g0)
plot_gens(loc_g0, loc_implantation)
cooperativity(loc_g0, loc_implantation, kappa, gamma)



