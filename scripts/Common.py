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

def EtaPhi(x,y,z):
    r = (x**2+y**2)**0.5
    theta = np.arctan(r/z)
    eta = -np.log(np.tan(theta/2))
    phi = np.arccos(x/r)
    phi[x<0] = 2*np.pi - phi[x<0]
    return eta, phi



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


from matplotlib.patches import Arc
from matplotlib.collections import PatchCollection

def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):

    if np.isscalar(c):
        kwargs.setdefault('color', c)
        c = None

    if 'fc' in kwargs:
        kwargs.setdefault('facecolor', kwargs.pop('fc'))
    if 'ec' in kwargs:
        kwargs.setdefault('edgecolor', kwargs.pop('ec'))
    if 'ls' in kwargs:
        kwargs.setdefault('linestyle', kwargs.pop('ls'))
    if 'lw' in kwargs:
        kwargs.setdefault('linewidth', kwargs.pop('lw'))
    # You can set `facecolor` with an array for each patch,
    # while you can only set `facecolors` with a value for all.

    zipped = np.broadcast(x, y, s)
    patches = [Circle((x_, y_), s_)
               for x_, y_, s_ in zipped]
    collection = PatchCollection(patches, **kwargs)
    if c is not None:
        c = np.broadcast_to(c, zipped.shape).ravel()
        collection.set_array(c)
        collection.set_clim(vmin, vmax)

    ax = plt.gca()
    ax.add_collection(collection)
    ax.autoscale_view()
    plt.draw_if_interactive()
    if c is not None:
        plt.sci(collection)
    return collection

