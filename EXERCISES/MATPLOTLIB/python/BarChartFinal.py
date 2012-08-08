import sys
import string
import datetime as dt
import numpy as np
import pylab as pl
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
#--function for parsing string into a datetime
def mkdate(text):
    return dt.datetime.strptime(text, '%m/%d/%Y')
#--modify default matplotlib settings
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
#--read data
metnames = ['date','Rain_inpd','ETP_mmpd','AirTMin_C','AirTMax_C']
d = np.genfromtxt( '..\\data\\MeterologicData.csv', skip_header=1, delimiter=',', \
                   missing_values=('MISSING','MISSING','MISSING','MISSING','MISSING'), \
                   filling_values=(dt.date(1900, 1, 1),0.0,0.0,np.NAN,np.NAN), \
                   names=metnames, dtype=None, converters={'date':mkdate} )
datemin = dt.date(d['date'].min().year  , 1, 1)
datemax = dt.date(d['date'].max().year+1, 1, 1)
#--create monthly totals for rainfall and ETP
on_date = d['date'][0]
monthly_data, c = [], [0.0, 0.0]
for ipos,t in enumerate( d['date'] ):
    if t.month != on_date.month or ipos == len( d['date'] ) - 1:
        t_month = t_date.month
        t_day = 1 #int( t_date.day / 2 )
        t_year = t_date.year
        monthly_data.append( [ dt.date(t_year, t_month, t_day), c[0], c[1], t_date.day ] )
        c[0] = 0.0
        c[1] = 0.0
        on_date = t
    c[0] += d['Rain_inpd'][ipos]
    c[1] += d['ETP_mmpd'][ipos]
    t_date = t
monthly_data = np.array( monthly_data )
#--create figures
#--how big to make the figure and where to place it
fwid, fhgt = 6.00, 4.50
flft, frgt = 0.075, 0.925
fbot, ftop = 0.10, 0.95
fig = pl.figure( figsize=(fwid, fhgt), facecolor='w' )
fig.subplots_adjust(wspace=0.25,hspace=0.25,left=flft,right=frgt,bottom=fbot,top=ftop)
#--matplotlib date specification
years, months = mdates.YearLocator(), mdates.MonthLocator()  #every year, every month
yearsFmt = mdates.DateFormatter('%Y')
#--define the first subplot
ax = fig.add_subplot(3,1,1)
#--plot the temperature data
ax.plot(pl.date2num(d['date']),d['AirTMin_C'], color='b', linewidth=0.7, label=r'T$_{MIN}$')
ax.plot(pl.date2num(d['date']),d['AirTMax_C'], color='r', linewidth=0.7, label=r'T$_{MAX}$')
#--legends and axes
leg = ax.legend(loc='upper left',ncol=2,labelspacing=0.25,columnspacing=1,\
                handletextpad=0.5,handlelength=2.0,numpoints=1)
leg._drawFrame=False 
ax.xaxis.set_major_locator(years), ax.xaxis.set_minor_locator(months)
ax.xaxis.set_major_formatter(yearsFmt)
ax.set_xlim(datemin, datemax)
ax.set_ylabel( r'Temperature $^{\circ}$C' )
ax.set_ylim(0,45)
#--define the second subplot
ax = fig.add_subplot(3,1,2)
#--plot the rainfall data
ax.bar(pl.date2num(monthly_data[:,0]),monthly_data[:,1]*25.4, \
       color='b', width=monthly_data[:,3], linewidth=0, label='Rainfall')
ax2 = ax.twinx()
ax2.plot(pl.date2num(monthly_data[:,0]),np.cumsum( monthly_data[:,1]*25.4/1000. ), color='k' )
#--axes
ax.xaxis.set_major_locator(years), ax.xaxis.set_minor_locator(months)
ax.xaxis.set_major_formatter(yearsFmt)
ax.set_xlim(datemin, datemax)
ax.set_ylabel( 'Rainfall mm' )
ax2.set_ylabel( 'Cumulative Rainfall m' )
#--define the third subplot
ax = fig.add_subplot(3,1,3)
#--plot the potential evapotranspiration data
ax.bar(pl.date2num(monthly_data[:,0]),monthly_data[:,2], \
       color='r', width=monthly_data[:,3], linewidth=0, label='Rainfall')
#--axes
ax.xaxis.set_major_locator(years), ax.xaxis.set_minor_locator(months)
ax.xaxis.set_major_formatter(yearsFmt)
ax.set_xlim(datemin, datemax)
ax.set_xlabel( 'Year' )
ax.set_ylabel( 'PET mm' )
#--output figure
#--png
outfigpng = '..\\figures\\MeterologicBar.png'
fig.savefig(outfigpng,dpi=300)
print 'created...', outfigpng
