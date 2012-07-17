import numpy as np
from datetime import datetime
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42 # this strange bit of code makes fonts 
                                  # editable in Adobe Illustator
import matplotlib.pyplot as plt
import re
import os

def NWIS_reader(infile):
    '''
    NWIS_reader(infile)
    A function to read in an NWIS file generated using USGS webservices.
    Mike Fienen - 7/16/2012
    <mnfienen *at* usgs *dot* gov>
    
    INPUT:
    infile --> the name of an input file in ZUSGS RDB (tab-delimited) format
    
    OUTPUT:
    indat --> a dictionary with keys corresponding to site numbers and each
            element being a dictionary with keys date and depth to water.
    '''
    # tell the user what's happening
    print 'Reading Data from file: %s' %(infile)
    #
    # set up a couple initial variables
    #
    # format for reading the date --> formats noted at 
    #        http://docs.python.org/library/datetime.html (bottom of the page)
    indatefmt = "%Y-%m-%d"
    
    
    # open the text file and read all lines into a variable "tmpdat"
    tmpdat = open(infile,'r').readlines()
    
    # make empty lists to temporarily hold the data
    Site_ID = []   # site ID
    dates = []     # date of measurement (daily values)
    DTW = []       # depth to water below land surface (feet)
    prov_code = [] # provisional code: [P] is provisional, [A] is accepted
    
    # loop over the input data, keep only proper data rows. Parse and assign to lists
    for lnum, line in enumerate(tmpdat):
        # first read the lookup information from the header of the file
        if ("data for the following" in line.lower()):
            nWells = int(re.findall("[0-9]+",line)[0])
            statnums = []
            countynums = []
            for cwell in np.arange(nWells):
                nextline = lnum+1+cwell
                tmp = tmpdat[nextline].strip().split()
                statnums.append(tmp[2])
                countynums.append(tmp[3])
            station_lookup = dict(zip(statnums,countynums))
                
        if (('usgs' in line.lower()) and ('#' not in line)):
            tmp = line.strip().split() # strip newline off the end and split on whitespace
            Site_ID.append(tmp[1])
            dates.append(datetime.strptime(tmp[2],indatefmt)) #convert date to a time tuple
            DTW.append(tmp[3])
            prov_code.append(tmp[4].lower()) # --> note conversion to lower case!


    Site_ID = np.array(Site_ID,dtype=str) # convert to a numpy array
                                          # keep as str to not lose trailing zeroes (!)
    DTW = np.array(DTW,dtype=float) # convert to numpy array as a float containing the measurements
    dates = np.array(dates,dtype=object) #convert to numpy array as object since these are time tuples
    prov_code = np.array(prov_code,dtype=str) # convert to a numpy array as string 
    unique_sites = np.unique(Site_ID) # get a unique list of the sites
    
    # make an empty dictionary to include the results
    indat = dict()
    # now loop over the unique sites and parse the results by site number
    for csite in unique_sites:
        cindices = np.nonzero(Site_ID == csite)[0] # find the indices for the current site
        indat[csite] = {'dates':dates[cindices],
                        'DTW':DTW[cindices],
                        'prov_code':prov_code[cindices]}
    # tell the user we are done!
    print "Reading %s complete!" %(infile)
    return indat,station_lookup
   
def NWIS_plotter(indat,station_lookup,plot_format,disp_plot=False):
    '''
    NWIS_plotter(indat,station_lookup,plot_format,disp_plot)
    
    A function to plot each hydrograph from an NWIS data query. The alternate name is used as the title
    Mike Fienen - 7/16/2012
    <mnfienen *at* usgs *dot* gov>
    
    INPUT:
    indat --> a dictionary of data returned from NWIS_reader
    station_lookup --> a dictionary linking station ID to station name
    plot_format --> format to save files of plots. can be '.png' or '.pdf'
    disp_plot --> a Boolean flag determining whether or not to display the plots onscreen
    
    OUTPUT:
    a set of files with plots of depth to water (reversing y axis) and named with station ID
    '''
    # check to see if there's already a figures subdirectory. If not, make one!
    if os.path.exists('figures')==False:
        os.mkdir('figures')

    for cstation in station_lookup.keys():
        # tell the user what's going on
        print 'plotting Station ID: %s' %(cstation)
        #
        # first parse all the data for the current station
        #
        cname = station_lookup[cstation] # find the name from the stationID lookup dictionary
        DTW = indat[cstation]['DTW'] # get the depth to water for the current station
        prov_code = indat[cstation]['prov_code'] # get the provisional/approved codes
        dates = indat[cstation]['dates'] # pull the dates as datetime objects
        p_inds = np.nonzero(prov_code=='p')[0]
        a_inds = np.nonzero(prov_code=='a')[0]

        #
        # then set up the figure and plot it
        #
        fig = plt.figure() # make a figure
        ax = fig.add_subplot(111)  # make a handle (ax) to the axes object in the figure
        plt.hold = True  # hold the figure to allow multiple plotting events
        if len(a_inds) > 0:
            plt.plot(dates[a_inds],DTW[a_inds],'b.')
        if len(p_inds) > 0:
            plt.plot(dates[p_inds],DTW[p_inds],'r.')
        ax.set_ylim([np.max(DTW),np.min(DTW)])
        
        # set the title and label the axes
        plt.title(cname)
        plt.ylabel('Depth to Water (feet)')
        plt.xlabel('Date')
        # rotate the xtick labels to avoid dates overlapping
        plt.xticks(rotation = 30)
        # finally, add a legend
        if len(p_inds) > 0 and len(a_inds) > 0:
            plt.legend(['Approved','Provisional'],loc='best')
        elif len(p_inds) > 0:
            plt.legend(['Provisional'],loc='best')
        elif len(a_inds) > 0:
            plt.legend(['Approved'],loc='best')
        plt.gcf().subplots_adjust(bottom=0.15) # make a little room for the date labels

        plt.savefig(os.path.join('figures',cstation + plot_format))
    if disp_plot:
        plt.show()
        
