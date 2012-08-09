import numpy as np
t0 = np.arange(0,11,1)
t1 = -np.arange(0,11,1)
for ipos in range(0,10):
    print t0[ipos], t1[ipos]

for ipos,(v1,v2) in enumerate( zip(t0,t1) ):
    print v1, v2

