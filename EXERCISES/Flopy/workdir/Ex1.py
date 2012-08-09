#Import packages
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
from subprocess import Popen


#Add flopy to the path and then import it
flopypath = '..\\flopy'
if flopypath not in sys.path:
    sys.path.append(flopypath)
from mf import *
from mfreadbinaries import mfhdsread, mfcbcread

#Grid and model information
nlay = 1
ncol = 21
nrow = 21
Lx = 19200.0
Ly = 19200.0
top = 0.0
bot = -100.0
kh = 1.00
kv = 1.00
ss = 1.0e-04
sy = 0.1
delr =  Lx / float(ncol - 1)
delc =  Ly / float(nrow - 1)
item3 = [[1,0,1,0]]
laytyp = 0
h1 = 48.
h2 = 40.
Qwell = -1000.

#Solver information
mxiter=100
iter1=50
hclose = 1.e-4
rclose = 1.e-2

#Temporal information
nper = 1
perlen = [1.0]
nstp = [1]
tsmult = [1.0]
steady = [True]

#Ibound and startinf heads
ibound = np.ones((nrow, ncol, nlay),'int')
ibound[:,0,:] = -1; ibound[:,-1,:] = -1
start = np.zeros((nrow, ncol, nlay))
start[:,0,:] = h1
start[:,-1,:] = h2

#Well data
wlist = [ [ nlay, (ncol - 1) / 2 + 1, (nrow - 1) / 2 + 1, 0.]  ]

#River data
rivstg = np.linspace(h1, h2, num=ncol)
rivcol = np.arange(ncol)
rivrow = np.sin(rivcol / 10.) * nrow / 3. + int(nrow / 2.)
rivlist = []
cond = 10.
rbot = 0.
for i in range(1, ncol-1):
    rivlist.append( [1, int(rivrow[i]), rivcol[i], rivstg[i], cond, rbot] )
rivlist = [rivlist]

name = 'mf'
os.system('del '+name+'.*')
ml = modflow(modelname=name, version='mf2005', exe_name='mf2005.exe')
discret = mfdis(ml,nrow=nrow,ncol=ncol,nlay=nlay,delr=delr,delc=delc,laycbd=0,
                top=top,botm=bot,nper=nper,perlen=perlen,nstp=nstp,
                tsmult=tsmult,steady=steady)
bas = mfbas(ml,ibound=ibound,strt=start)
lpf = mflpf(ml, hk=kh, vka=kv, ss=ss, sy=sy, laytyp=laytyp)
well = mfwel(ml, layer_row_column_Q=wlist)
riv = mfriv(ml, layer_row_column_Q=rivlist, irivcb=53)
oc = mfoc(ml,ihedfm=2,item3=item3)
pcg = mfpcg(ml,hclose=hclose,rclose=rclose,mxiter=mxiter,iter1=iter1)

#write input and run the model
ml.write_input()
Popen(['mf2005.exe', name + '.nam']).communicate()[0]


times, cbc, stringscbc = mfcbcread(ml, compiler='i').read_all(name + '.cbc')
times, head, stringshds = mfhdsread(ml, compiler='i').read_all(name + '.hds')

try:
    plt.close()
except:
    pass
plt.figure()
extent = (0, Lx, 0, Ly)
plt.imshow(head[0][:, :, 0], interpolation='nearest', extent=extent)
plt.title('Base Case Head')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig('base.png')

rivleak = cbc[0][3][:, :, 0]
netrivleakbase = rivleak.sum()
try:
    plt.close()
except:
    pass
plt.figure()
plt.imshow(rivleak, interpolation='nearest', extent=extent)
plt.colorbar()
plt.title('Base Case River Leakage')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig('baseleak.png')

cf = np.zeros((nrow, ncol), dtype=float)
for i in xrange(nrow):
    for j in xrange(ncol):
        wlist = [ [ 1, i + 1, j + 1, Qwell]  ]
        ml.remove_package('WEL')
        mfwel(ml, layer_row_column_Q=wlist)
        ml.write_input()
        Popen(['mf2005.exe', name + '.nam']).communicate()[0]
        print 'Model completed.'
        times, cbc, stringscbc = mfcbcread(ml, compiler='i').read_all(name + '.cbc')
        rivleak = cbc[0][3]
        netrivleak = rivleak.sum()
        cf[i, j] = (netrivleak - netrivleakbase) / netrivleakbase
        print i + 1, j + 1, netrivleak, netrivleakbase, cf[i, j]
        
try:
    plt.close()
except:
    pass
plt.figure()
plt.imshow(cf, interpolation='nearest', extent=extent)
plt.colorbar()
plt.title('Capture Fraction')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig('capture.png')
