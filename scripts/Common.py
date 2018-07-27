from pylab import *

def getBaseDir(isLocal=True):
    if isLocal:
        # on my local macbook
        baseDir = '/Users/zihengchen/Documents/HGCal/'
    else:
        # on bahamut
        baseDir = '/home/zchen/Documents/HGCal/'
    return baseDir


def getTauDecayMode(gen_id):

    gen_id = np.unique(np.abs(gen_id))
    gen_id = gen_id[gen_id!=22]
    
    if 13 in gen_id:
        tauDecayMode = 1
    elif 211 in gen_id:
        tauDecayMode = 2
    else:
        tauDecayMode = 0
        
    return tauDecayMode


def truncatedCone(eta0,eta1,z0,z1):
    R,r = 200,400
    theta0 = 2*np.arctan(np.exp(-eta0))
    theta1 = 2*np.arctan(np.exp(-eta1))
        
    phi = np.linspace(0, 2 * np.pi, 120)
    rad = np.linspace(0, 2 * np.pi, 120)
    phi, rad = np.meshgrid(phi,rad)
    
    z   = ((z0+z1)/2 + r*np.sin(rad)).clip(z0,z1)
    rho = (R+r*np.cos(rad))
    
    for i in range(120):
        for j in range(120):
            rhomax = z[i,j]*np.tan(theta0)
            rhomin = z[i,j]*np.tan(theta1)
            if rho[i,j] > rhomax:
                rho[i,j] = rhomax
            if rho[i,j] < rhomin:
                rho[i,j] = rhomin
    rho = rho.clip(0,250)
                
    x = rho*np.cos(phi) 
    y = rho*np.sin(phi) 
    
    return x,y,z