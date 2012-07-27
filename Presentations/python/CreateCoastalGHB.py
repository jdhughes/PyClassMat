import numpy as np
import MFArrayUtil as au
#--function for calculating equivalent freshwater head
def eqfwh( rho, h, z ):
    return ( rho / 1000. ) * h - ( ( rho - 1000. ) / 1000. ) * min( h, z )
#--main script
#--spatial dimensions
nlay, nrow, ncol  = 1, 41, 40
dx, dy = 500.0, 500.0 #m
#--temporal dimensions
nper = 3
#--boundary condition data
icbc, start_coast = 0, 36
kh    = 10.000 #m/d
cond  = kh * dx * dy
#--read MODFLOW data from external files
ibound  = au.loadArrayFromFile(nrow,ncol,'..\\ref\\ibound.ref')
top     = au.loadArrayFromFile(nrow,ncol,'..\\ref\\top.ref')
#--ghb dataset
nghb = 0
for ir in range(0,nrow):
    for ic in range(0,ncol):
        if ibound[ir,ic] == 2:
            nghb += 1
f = open('Model.ghb','w')
#--dataset 0
f.write( '#Coastal Aquifer GHB Package\n' )
#--dataset 1
f.write( '{0:10d}{1:10d}  NOPRINT\n'.format( nghb, icbc ) )
#--write header for ghb file -- stress period 1  
f.write( '{0:10d}         0          #STRESS PERIOD {1:05d}\n'.format( nghb, 1 ) )
for ir in range(0,nrow):
    for ic in range(0,ncol):
        if ibound[ir,ic] == 2:
            f.write( ' {0:9d} {1:9d} {2:9d} {3:9.5f} {4:9.3g}\n'.format(nlay,ir+1,ic+1, \
                     eqfwh( 1025., 0.0, top[ir,ic]),cond ) )
#--reuse data for the remaining stress period(s)
for iper in range(1,nper):
    f.write( '{0:10d}         0          #STRESS PERIOD {1:05d}\n'.format(-1,iper+1) )
f.close()
