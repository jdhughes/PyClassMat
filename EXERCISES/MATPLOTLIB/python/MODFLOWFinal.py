import sys
import os
import math
import numpy as np
import pylab

import MFArrayUtil as au
import MFBinaryClass as mfb 

#preliminary figure specifications
from matplotlib.pyplot import *
import matplotlib as mpl
from matplotlib.font_manager import FontProperties

mpl.rcParams['font.sans-serif']          = 'Univers 57 Condensed' #'Arial'
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

#--problem size
nlay,nrow,ncol = 1,41,40
#--default data if command line argument not defined for variable
head_file = '..\\data\\CoastalAquifer.hds'
#--get available times in the head file
get_cell = 1
headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
t = headObj.get_gage(get_cell)
ntimes = t.shape[0]
mf_times = np.zeros( (ntimes), np.float )
for i in range(0,ntimes):
    mf_times[i] = t[i,0]

#--create a time-series plot of head
headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
get_cell = mfb.icrl_from_kij(1,18,31,nlay,nrow,ncol)
t = headObj.get_gage(get_cell)
ztf = figure(figsize=(4, 2), facecolor='w')
ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.15,right=0.95,bottom=0.15,top=0.95)
ax = ztf.add_subplot(1,1,1)
hp = ax.plot(mf_times/365.25-100.,t[:,1])
ax.set_xlim(0,50)
xlabel('Time since the beginning of groundwater withdrawls (years)')
ylabel('Head (m)')
output_name = '..\\figures.MF\\Cell_{0}.png'.format( get_cell )
ztf.savefig(output_name,dpi=300)
#--create a time-series plot of drawdown
h0 = t[:,1].max()
ztf = figure(figsize=(4, 2), facecolor='w')
ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.15,right=0.95,bottom=0.15,top=0.95)
ax = ztf.add_subplot(1,1,1)
hp = ax.plot(mf_times/365.25-100.,h0-t[:,1])
ax.set_xlim(0,50)
xlabel('Time since the beginning of groundwater withdrawls (years)')
ylabel('Drawdown (m)')
output_name = '..\\figures.MF\\Cell_{0}_drawdown.png'.format( get_cell )
ztf.savefig(output_name,dpi=300)

#--make a map 
#--coordinate information
dx,dy   = 500., 500.
xcell = np.arange(dx/2.,(ncol*dx)+dx/2.0,dx)
ycell = np.arange(dy/2.,(nrow*dy)+dy/2.0,dy)
Xcell,Ycell = np.meshgrid(xcell,ycell)
xedge = np.arange(0.0,float(ncol)*dx+0.001,dx)
yedge = np.arange(0.0,float(nrow)*dy+0.001,dy)
Xedge,Yedge = np.meshgrid(xedge,yedge)
xmin,xmax = 0.0,float(ncol)*dx
ymin,ymax = 0.0,float(nrow)*dy
#--common data for each figure
hdcontour  = np.arange(0.0,10.0,0.25)  
#--create figures for each output time
for on_time in mf_times:
    #--build output file name
    output_name = '..\\figures.MF\\Head_{0:05d}.png'.format( int( on_time ) )
    #--read head data - final zeta surface
    headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
    totim,kstp,kper,h,success = headObj.get_record(on_time)
    hd = np.copy( h[0,:,:] )
    #--invert rows for plotting with pcolor
    hd       = np.flipud(hd)
    #--calculate ranges
    minh, maxh = np.min(hd), np.max(hd)
    #--print summary of min and max head and zeta
    print 'Head                 [{0:10.3f},{1:10.3f}]'.format(minh,maxh)
    #-Make figures
    print 'creating figure...{0}'.format( output_name )
    #--figure
    ztf = figure(figsize=(3, 3), facecolor='w')
    ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.15,right=0.95,bottom=0.15,top=0.95)
    ax = ztf.add_subplot(1,1,1,aspect='equal')
    iyears = int( on_time / 365. ) - 100
    ctime = 'years'
    if iyears == 1:
        ctime = 'year'
    ctitle = 'Groundwater head (m) after {0:5d} {1}'.format( iyears, ctime )
    text(0.0,1.01,ctitle,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    #hp = ax.pcolor(Xedge,Yedge,hd,vmin=0,vmax=2,cmap='jet_r',alpha=1.0,edgecolors='None')
    hp = ax.imshow(np.flipud(hd),vmin=0,vmax=2,cmap='jet_r',alpha=1.0,extent=[xmin,xmax,ymin,ymax])
    ch = ax.contour(xcell,ycell,hd,levels=hdcontour,colors='k',linewidths=1)
    ax.clabel(ch,inline=1,fmt='%5.2f',fontsize=6)
    #--plot limits
    ax.set_xlim(xmin,xmax), ax.set_ylim(ymin,ymax)
    xlabel('Column distance (m)')
    ylabel('Row distance (m)')
    #--save the figure
    ztf.savefig(output_name,dpi=300)


