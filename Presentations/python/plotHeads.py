import sys
import os
import subprocess
import numpy as np
import pylab
import MFArrayUtil as au
import MFBinaryClass as mfb 
#preliminary figure specifications
from matplotlib.pyplot import *
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
mpl.rcParams['font.sans-serif']          = 'Univers 57 Condensed'
mpl.rcParams['font.serif']               = 'Times'
mpl.rcParams['font.cursive']             = 'Zapf Chancery'
mpl.rcParams['font.fantasy']             = 'Comic Sans MS'
mpl.rcParams['font.monospace']           = 'Courier New'
mpl.rcParams['pdf.compression']          = 0
mpl.rcParams['pdf.fonttype']             = 42
ticksize = 6
mpl.rcParams['legend.fontsize']  = 6
mpl.rcParams['axes.labelsize']   = 8
mpl.rcParams['xtick.labelsize']  = ticksize
mpl.rcParams['ytick.labelsize']  = ticksize
#--default data if command line argument not defined for variable
base_dir, base_name, extension  = '..\\Figures.MF\\', 'MF_Results', 'png'
head_file = '..\\Results.MF\\CoastalAquifer.hds'
#--problem size
nlay, nrow, ncol = 1, 41, 40
#--coordinate information
dx, dy = 500., 500.
xOff, yOff = 0.0, 0.0
xcell = np.arange(xOff+dx/2.,xOff+(ncol*dx)+dx/2.0,dx)
ycell = np.arange(yOff+dy/2.,yOff+(nrow*dy)+dy/2.0,dy)
Xcell,Ycell = np.meshgrid(xcell,ycell)
xedge = np.arange(xOff,xOff+float(ncol)*dx+0.001,dx)
yedge = np.arange(yOff,yOff+float(nrow)*dy+0.001,dy)
Xedge,Yedge = np.meshgrid(xedge,yedge)
xmin,xmax = xOff, xOff+float(ncol)*dx
ymin,ymax = yOff, yOff+float(nrow)*dy
#--read MODFLOW data from external files and invert for plotting
ibound  = au.loadArrayFromFile(nrow,ncol,'..\\ref\\ibound.ref')
ibound   = np.flipud(ibound)
#--get available times
headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
t = headObj.get_gage(1)
ntimes = t.shape[0]
mf_times = np.zeros( (ntimes), np.float )
for i in range(0,ntimes):
    mf_times[i] = t[i,0]
#--common data for each figure
hdcontour  = np.arange(0.0,10.0,0.25)
struct_loc = [20,30]
well_loc = np.array( [ [23,30], [13,14] ] )
fnames = [] #list of output file names
#--create figures for each output time
for ipos,on_time in enumerate( mf_times ):
    #--build output file name
    output_name = '{0}{1}_{2:05d}.{3}'.format(base_dir,base_name,int(ipos),extension)
    fnames.append( output_name ) 
    #--read head data
    headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
    totim,kstp,kper,h,success = headObj.get_record(on_time)
    hd = np.copy( h[0,:,:] )
    #--invert rows for plotting and mask data in inactive areas
    hd       = np.flipud(hd)
    hd       = np.ma.masked_where(ibound<1,hd)
    #--calculate ranges
    minh, maxh = np.min(hd), np.max(hd)
    print 'Head                 [{0:10.3f},{1:10.3f}]'.format(minh,maxh)
    #-Make figures
    print 'creating figure...{0}'.format( output_name )
    #--figure
    ztf = figure(figsize=(4.0,4.0), facecolor='w')
    ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.1,right=0.9,bottom=0.1,top=0.9)
    ax = ztf.add_subplot(1,1,1,aspect='equal')
    iyears = int( on_time / 365. )
    ctime = 'years'
    if iyears == 1:
        ctime = 'year'
    ctitle = 'Groundwater head (m) after {0:5d} {1}'.format( iyears, ctime )
    text(0.0,1.01,ctitle,\
         horizontalalignment='left',verticalalignment='bottom',size=7,\
         transform=ax.transAxes)
    hp = ax.pcolor(Xedge,Yedge,hd,\
                   vmin=0,vmax=2,cmap='jet_r',alpha=1.0,edgecolors='None')
    ch = ax.contour(xcell,ycell,hd,\
                    levels=hdcontour,colors='k',linewidths=1)
    ax.clabel(ch,inline=1,fmt='%5.2f',fontsize=6)
    ax.plot([xedge[0],xedge[35]],[ycell[20],ycell[20]],linewidth=1,color='b',label='River')
    ax.plot(xcell[struct_loc[1]],ycell[struct_loc[0]],'gs',markersize=4,label='Structure')
    ax.plot(xcell[well_loc[0,1]],ycell[well_loc[0,0]],'ko',markersize=3,label='PW-1')
    ax.plot(xcell[well_loc[1,1]],ycell[well_loc[1,0]],'ko',markersize=3,label='PW-2')
    #--plot limits
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    xlabel('Column distance (m)')
    ylabel('Row distance (m)')
    #--save figure
    ztf.savefig(output_name,dpi=600)
    close(ztf)
#--animate head data
coutf = '{0}{1}.swf'.format(base_dir,base_name)
cline = 'ffmpeg.exe -i {0}{1}_%05d.png {2} -y'.format( base_dir,base_name,coutf )
try:
    os.remove(coutf)
except:
    print 'could not remove...{0}'.format( coutf )
subprocess.call(cline, stdin=None, stdout=None, stderr=None, shell=False)
#--delete temporary png files
for f in fnames:
    os.remove(f)
