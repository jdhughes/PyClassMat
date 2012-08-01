import numpy as np
import pylab as pl
import matplotlib as mpl
#--load flow data
q = np.genfromtxt( '..\\data\\USInflow.dat', skip_header=4 )
#--create figure of upstream inflow
fig = pl.figure( figsize=(6.0, 2.0), facecolor='w' )
#--define the subplot
ax = fig.add_subplot(1,1,1)
#--plot the data
ax.plot(q[:,0],q[:,1])
#--output figure
#--png
fig.savefig('..\\figures\\SuperSimplePlot.png',dpi=300)
