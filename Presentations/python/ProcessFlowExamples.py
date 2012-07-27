import numpy as np
#--load flow data
q = np.genfromtxt( 'USInflow.dat', skip_header=1 )
#--determine sizes
ntimes, ncol = q.shape[0], q.shape[1]
print 'Number of times:   {0:10d}\nNumber of entries: {1:10d}'.format( ntimes, ncol )
#--while iteration with break and continue
ipos = 0
while True:
    #--only print last line
    if ipos+1 < ntimes:
        #--increment ipos by one
        ipos += 1
        continue
    #--print data
    print '{0:25s}: {1}, {2}, {3}'.format( 'while iteration', ipos+1, q[ipos,0], q[ipos,1] )
    #--terminate after printing last element
    break
#--range iterator - range creates a list
for ipos in range(0,ntimes):
    #--only print last line
    if ipos+1 < ntimes:
        continue
    #--print data
    print '{0:25s}: {1}, {2}, {3}'.format( 'range iteration', ipos+1, q[ipos,0], q[ipos,1] )
#--xrange iterator - xrange is a generator
for ipos in xrange(0,ntimes):
    #--only print last line
    if ipos+1 < ntimes:
        continue
    #--print data
    print '{0:25s}: {1}, {2}, {3}'.format( 'xrange iteration', ipos+1, q[ipos,0], q[ipos,1] )
#--element iterator
ipos = 0
for t in q:
    #--increment ipos by one
    ipos += 1
    #--only print last line
    if ipos < ntimes:
        continue
    #--print data
    print '{0:25s}: {1}, {2}, {3}'.format( 'element iteration', ipos, t[0], t[1] )
#--enumeration iterator
for ipos,t in enumerate(q):
    #--only print last line
    if ipos+1 < ntimes:
        continue
    print '{0:25s}: {1}, {2}, {3}'.format( 'enumeration iteration', ipos+1, t[0], t[1] )
#--enumeration iterator with zip
v0, v1 = np.copy( q[:,0] ), np.copy( q[:,1] )
for ipos,( t0, t1 ) in enumerate( zip( v0,v1 ) ):
    #--only print last line
    if ipos+1 < ntimes:
        continue
    print '{0:25s}: {1}, {2}, {3}'.format( 'enumeration/zip iteration', ipos+1, t0, t1 )
