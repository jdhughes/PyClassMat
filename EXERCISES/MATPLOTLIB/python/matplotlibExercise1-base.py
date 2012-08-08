import datetime as dt
import numpy as np
import pylab as pl
import matplotlib as mpl
#--load flow data
q = np.genfromtxt( '..\\data\\06719505.txt', \
                   names=['date','discharge'], dtype=[dt.datetime,'<f8'])
#--create a figure of the discharge for the last year
pl.figure( figsize=(6.0, 5.0), facecolor='w' )
#--plot the data
pl.plot(q['discharge'])
#
pl.xlabel('Days')
pl.ylabel(r'Discharge ft$^3$/s')
pl.xlim(0,365)
#--output figure
pl.savefig('..\\figures\\matplotlibExercise1-base.png',dpi=300)
#--show the plot
pl.show()
