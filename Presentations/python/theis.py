import numpy as np
from scipy.special import expn

def theis(Q, T, S, t, r):
    return Q / 4. / np.pi / T * expn(1, r ** 2 * S / 4. / T / t)

T = 1.; S = 0.001; t = 10.; rw = 0.01
xmin = -200; xmax = 200; nx = 100; ymin = -200; ymax = 200; ny = 100
x, y = np.meshgrid(np.linspace(xmin, xmax, nx), np.linspace(ymin, ymax, ny))
wells = [ [25, 30, 3], [50, 50, 3], [75, 30, 3] ]
ddn = np.zeros( x.shape, dtype=float)
for xw, yw, Qw in wells:
    print 'Processing Well: x={0}, y={1}, Q={2}'.format(xw, yw, Qw)
    r = np.sqrt((x - xw) ** 2 + (y - yw) ** 2)
    r = np.where(r > rw, r, rw)
    ddn = ddn + theis(Qw, T, S, t, r)
    
from matplotlib.pyplot import *
try:
    close('all')
except:
    pass
subplot(1, 1, 1, aspect='equal')
contourf(x, y, ddn)
colorbar(shrink=0.5)
show()
