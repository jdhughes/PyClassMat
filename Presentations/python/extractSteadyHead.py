import numpy as np
import MFBinaryClass as mfb 
#--problem size
nlay, nrow, ncol = 1, 41, 40
nper, nstp = 1, 100
#--name of MODFLOW head file
head_file = '..\\Results.SWI\\CoastalAquifer.hds'
#--read head data
#--create instance of head object from MFBinaryClass
headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
#--read array
totim,kstp,kper,h,success = headObj.get_record(nstp,nper)
#--save array or print error message
if success:
    np.savetxt('..\\ref\\steady_ihead.ref',h[0,:,:])
else:
    print 'Could not read Stress Period {0} Time Step {1}\n  from {2}'.format(nper,nstp,\
                                                                              head_file)
#--read zeta surface
zeta_file = '..\\Results.SWI\\CoastalAquifer.zta'
#--create instance of CBB object from MFBinaryClass
zetaObj = mfb.MODFLOW_CBB(nlay,nrow,ncol,zeta_file)
findsurf = '    ZETAPLANE  1'
z,totim,success = zetaObj.get_record(findsurf,kstp,kper)    
#--save array or print error message
if success:
    np.savetxt('..\\ref\\steady_zeta.ref',z[0,:,:])
else:
    print 'Could not read Stress Period {0} Time Step {1}\n  from {2}'.format(nper,nstp,head_file)
