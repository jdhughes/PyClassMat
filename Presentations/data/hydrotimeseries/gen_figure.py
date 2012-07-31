# Python script to make bar plot
# from PEST smp files.
#
#==============================================================================
# Requirements
# For Windows OS, need to install GhostScript in order to append PDFs
#
#==============================================================================
# Import Python modules
import datetime
import numpy
import matplotlib
import os
from pylab import *
from matplotlib.dates import *
from matplotlib.font_manager import FontProperties
import matplotlib.ticker as ticker

#==============================================================================
#set the start and end date range
date1 = datetime.date(1950,1,1)
date2 = datetime.date(2005,12,31)

# the tick locators and formatters
majortick   = YearLocator(10, month=1, day=1) #every 10 years on jan 1
minortick   = YearLocator(1, month=1, day=1) #every 1 year on jan 1
months  = MonthLocator()
MonthsFmt = DateFormatter('%b %d')
yearsFmt = DateFormatter('%Y')

#time series data
r = csv2rec('data.csv') #matplotlib.mlab csv reader

#g853 heads
g853 = csv2rec('g853.csv')

#concentrations
g2054c = csv2rec('g2054c.csv')
g2055c = csv2rec('g2055c.csv')
g2055Ac = csv2rec('g2055Ac.csv')
g2062c = csv2rec('g2062c.csv')
g2063c = csv2rec('g2063c.csv')
g2064c = csv2rec('g2064c.csv')

graphcolor='#FFFFCC'
fig1=figure(num=1,figsize=(8,11.5))
clf()

ax1=subplot(4,1,1,axisbg=graphcolor)
#xmin=r.start_date.min()
xmin=date2num(datetime.date(1940,1,1))
xmax=date2num(r.end_date.max())

#==============================================================================
#plot rainfall histogram
#==============================================================================

#bar of daily values
ax1.bar(r.start_date,r.rainfall*1000,width=r.width,bottom=0,color='blue',edgecolor='blue',label='monthly average')

#calculate and plot average annual rainfall totals
X=([])
for i in range(1941,2006):
	X.append(date2num(datetime.date(int(i),6,15)))
Y = zeros(2006)
for i in range(0,782):
	year=r.mid_date[i].year
	Y[year]=Y[year] + r.rainfall[i]*r.width[i]
Y=Y*100 #convert to centimeters per year
#annual averages
ax2 = ax1.twinx()
ax2.plot(X,Y[1941:2006],color='red', linestyle='solid', marker='o',markersize=3.,label='annual average')
#annual average
avgx=array([xmin,xmax])
avg=average(Y[1941:2006])
avgy=array([avg,avg])
ax2.plot(avgx,avgy,color='red', linestyle='dashed', label='period average')

#set axis limits
ax1.set_ylim(0,30)
ax2.set_ylim(0,350)

#legend
handles1,labels1=ax1.get_legend_handles_labels()
handles2,labels2=ax2.get_legend_handles_labels()
handles=handles1+handles2
labels=labels1+labels2
legend(handles,labels,loc=0,ncol=1, prop = FontProperties( size=10, family = 'arial' ))

#set x axis information
ax1.xaxis.set_major_locator(majortick)
ax1.xaxis.set_major_formatter(yearsFmt)
ax1.xaxis.set_minor_locator(minortick)
ax1.set_xlim(xmin,xmax)

axisfontsize=10
axisfontname='arial'
axisfontweight='bold'
axisfontstyle='normal'
ytext=ax1.set_ylabel('AVERAGE MONTHLY\nRAINFALL ('+r'$mm/d$'+')',
											#horizontalalignment='center',
											verticalalignment='center',
											multialignment='center',
											fontsize=axisfontsize,
											fontname=axisfontname,
											fontweight=axisfontweight,
											fontstyle=axisfontstyle)
for t1 in ax1.get_yticklabels():
	t1.set_fontsize(10)

#xtext=ax1.set_xlabel('YEAR',
#											#horizontalalignment='center',
#											#verticalalignment='baseline',
#											fontsize=axisfontsize,
#											fontname=axisfontname,
#											fontweight=axisfontweight,
#											fontstyle=axisfontstyle)
for t1 in ax1.get_xticklabels():
	t1.set_fontsize(10)

ytext=ax2.set_ylabel('AVERAGE ANNUAL\nRAINFALL ('+r'$cm/yr$'+')',
											#horizontalalignment='center',
											verticalalignment='center',
											multialignment='center',
											fontsize=axisfontsize,
											fontname=axisfontname,
											fontweight=axisfontweight,
											fontstyle=axisfontstyle)
for t1 in ax2.get_yticklabels():
	t1.set_fontsize(10)


#==============================================================================
#plot pompano withdrawals
#==============================================================================
ax3=subplot(4,1,2,axisbg=graphcolor)

ax3.bar(r.start_date,abs(r.palmaire),width=r.width,bottom=abs(r.pompeast),color='red',edgecolor='red',label='Palm Aire')
ax3.bar(r.start_date,abs(r.pompeast),width=r.width,bottom=0,color='blue',edgecolor='blue',label='Pompano East')

#set x axis information
ax3.xaxis.set_major_locator(majortick)
ax3.xaxis.set_major_formatter(yearsFmt)
ax3.xaxis.set_minor_locator(minortick)
ax3.set_xlim(xmin,xmax)

#set y axis
ax3.set_ylim(0,100000)

#formatter=ticker.LogFormatterMathtext(base=10.,labelOnlyBase=False)
#formatter=ticker.ScalarFormatter(useMathText=True)
#ax3.yaxis.set_powerlimits((-1,1))
formatter=ticker.FormatStrFormatter('%1.g')
ax3.yaxis.set_major_formatter(formatter)
x0='0'
x1='2x10' +r'$^4$'
x2='4x10' +r'$^4$'
x3='6x10' +r'$^4$'
x4='8x10' +r'$^4$'
x5='1x10'+r'$^5$'
ax3.yaxis.set_ticklabels((x0,x1,x2,x3,x4,x5))
ytext=ax3.set_ylabel('AVERAGE MONTHLY\nWITHDRAWAL ('+r'$m^3/d$'+')',
											horizontalalignment='right',
											verticalalignment='center',
											multialignment='center',
											fontsize=axisfontsize,
											fontname=axisfontname,
											fontweight=axisfontweight,
											fontstyle=axisfontstyle)
for t1 in ax3.get_yticklabels():
	t1.set_fontsize(10)



#xtext=ax3.set_xlabel('YEAR',
#											#horizontalalignment='center',
#											#verticalalignment='baseline',
#											fontsize=axisfontsize,
#											fontname=axisfontname,
#											fontweight=axisfontweight,
#											fontstyle=axisfontstyle)
for t1 in ax3.get_xticklabels():
	t1.set_fontsize(10)

#legend
handles,labels=ax3.get_legend_handles_labels()
legend(handles,labels,loc=0, ncol=1,prop = FontProperties( size=10, family = 'arial' ))

#==============================================================================
#plot stages
#==============================================================================
hillsboro = csv2rec('hillsboro.csv')
cypressck = csv2rec('cypressck.csv')
ax4=subplot(4,1,3,axisbg=graphcolor)
plot(r.start_date,r.atlanticstage,color='blue',label='Atlantic Ocean')
plot(hillsboro.start_date,hillsboro.waterlevel,color='green',label='Hillsboro Canal')
plot(cypressck.start_date,cypressck.waterlevel,color='orange',label='Cypress Creek Canal')
plot(g853.date,g853.waterlevel,color='red',label='G-853')

#set y axis range
ax4.set_ylim(-2,5)

#set x axis information
ax4.xaxis.set_major_locator(majortick)
ax4.xaxis.set_major_formatter(yearsFmt)
ax4.xaxis.set_minor_locator(minortick)
ax4.set_xlim(xmin,xmax)

ytext=ax4.set_ylabel('WATER LEVEL ('+r'$m$'+')',
											#horizontalalignment='center',
											verticalalignment='center',
											multialignment='center',
											fontsize=axisfontsize,
											fontname=axisfontname,
											fontweight=axisfontweight,
											fontstyle=axisfontstyle)
for t1 in ax4.get_yticklabels():
	t1.set_fontsize(10)

#xtext=ax4.set_xlabel('YEAR',
#											#horizontalalignment='center',
#											#verticalalignment='baseline',
#											fontsize=axisfontsize,
#											fontname=axisfontname,
#											fontweight=axisfontweight,
#											fontstyle=axisfontstyle)
for t1 in ax4.get_xticklabels():
	t1.set_fontsize(10)

#legend
handles,labels=ax4.get_legend_handles_labels()
legend(handles,labels,loc=0, ncol=2,prop = FontProperties( size=10, family = 'arial' ))


#==============================================================================
#plot concentrations
#==============================================================================
ax5=subplot(4,1,4,axisbg=graphcolor)
plot(g2054c.date,g2054c.tds,color='red', linestyle='solid', marker='o',markersize=3.,label='G-2054')
plot(g2055c.date,g2055c.tds,color='blue', linestyle='solid', marker='o',markersize=3.,label='G-2055')
plot(g2055Ac.date,g2055Ac.tds,color='green', linestyle='solid', marker='o',markersize=3.,label='G-2055A')
#plot(g2062c.date,g2062c.tds,color='brown', linestyle='solid', marker='o',markersize=3.,label='G-2062')
plot(g2063c.date,g2063c.tds,color='orange', linestyle='solid', marker='o',markersize=3.,label='G-2063')
#plot(g2064c.date,g2064c.tds,color='green', linestyle='solid', marker='o',markersize=3.,label='G-2064')



#set x axis information
ax5.xaxis.set_major_locator(majortick)
ax5.xaxis.set_major_formatter(yearsFmt)
ax5.xaxis.set_minor_locator(minortick)
ax5.set_xlim(xmin,xmax)
                                                         
ytext=ax5.set_ylabel('TDS ('+r'$kg/m^3$'+')',
											#horizontalalignment='center',
											verticalalignment='center',
											multialignment='center',
											fontsize=axisfontsize,
											fontname=axisfontname,
											fontweight=axisfontweight,
											fontstyle=axisfontstyle)
for t1 in ax5.get_yticklabels():
	t1.set_fontsize(10)

xtext=ax5.set_xlabel('YEAR',
											#horizontalalignment='center',
											#verticalalignment='baseline',
											fontsize=axisfontsize,
											fontname=axisfontname,
											fontweight=axisfontweight,
											fontstyle=axisfontstyle)
for t1 in ax5.get_xticklabels():
	t1.set_fontsize(10)

#legend
handles,labels=ax5.get_legend_handles_labels()
legend(handles,labels,loc=0, ncol=1,prop = FontProperties( size=10, family = 'arial' ))


show()
savefig('fig01.png',dpi=300,orientation='portrait',format='PNG')
savefig('fig01.pdf',orientation='portrait',format='PDF')