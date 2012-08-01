import sys
import string
import math
import numpy as np
import pylab as pl
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
#--general specification data for matplotlib
mpl.rcParams['font.sans-serif']          = 'Univers 57 Condensed'
mpl.rcParams['font.serif']               = 'Times'
mpl.rcParams['font.cursive']             = 'Zapf Chancery'
mpl.rcParams['font.fantasy']             = 'Comic Sans MS'
mpl.rcParams['font.monospace']           = 'Courier New'
mpl.rcParams['mathtext.default']         = 'regular'
mpl.rcParams['pdf.compression']          = 0
mpl.rcParams['pdf.fonttype']             = 42
#--figure text sizes
mpl.rcParams['legend.fontsize']  = 7
mpl.rcParams['axes.labelsize']   = 8
mpl.rcParams['xtick.labelsize']  = 7
mpl.rcParams['ytick.labelsize']  = 7
#--create upstream inflow data
#--temporal dimensions
nper    = 365 * 2 + 1
ntsp    = np.ones( (nper), np.int )
tsp_len = 1.0 #day
tmax    = float( nper ) * tsp_len
simtime = np.arange(0.0,tmax+2.*tsp_len,tsp_len)
#--generate a sinusoidal inflow function
q = np.zeros( (len(simtime)), np.float )
qbase, qptrb = 75.00, 25.00
tp   = 365.
ipos = 0
for ipos,t in enumerate( simtime ):
    qp = qptrb * math.sin( 2.0 * math.pi * t / tp )
    q[ipos] = qbase + qp
#--create figure of upstream inflow
#--how big to make the figure and where to place it
fwid, fhgt = 6.00, 1.50
flft, frgt = 0.10, 0.95
fbot, ftop = 0.20, 0.95
fig = pl.figure( figsize=(fwid, fhgt), facecolor='w' )
fig.subplots_adjust(wspace=0.25,hspace=0.25,left=flft,right=frgt,bottom=fbot,top=ftop)
#--define the subplot
ax = fig.add_subplot(1,1,1)
#--plot the data
ax.plot([0,10], [qbase,qbase], color='0.5', linewidth=0.5, label='_Zero')
ax.plot(simtime/365,q, color='b', linewidth=1, label='Inflow', marker='o', markevery=28)
#--titles and axes
ax.set_ylabel( r'Inflow $m^3/s$' )
ax.set_ylim(25,125)
ax.set_xlabel('Time,  years')	
ax.set_xlim(0,2)
ax.set_xticks( np.arange(0,3,1) )
#--output figure
#--png
outfigpng = '..\\figures\\Inflow.png'
fig.savefig(outfigpng,dpi=300)
print 'created...', outfigpng
#--pdf
outfigpdf = '..\\figures\\Inflow.pdf'
fig.savefig(outfigpdf,dpi=300)
print 'created...', outfigpdf
#--create output file
ofile = '..\\data\\USInflow.dat'
f = open(ofile,'w')
cline = '#Upstream inflow in cubic meters per second (cms)\n#convert cms to cubic feet per day for MODFLOW using SCALE below\nSCALE 86400.0\n#          time         inflow\n'
f.write(cline)
for ipos,t in enumerate( zip( simtime, q ) ):
    f.write( '{0:15.7g}{1:15.7g}\n'.format( t[0],t[1] ) )
f.close()
