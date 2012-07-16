import numpy as np
from datetime import datetime
import time



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
    #
    # set up a couple initial variables
    #
    # format for reading the date --> formats noted at 
    #        http://docs.python.org/library/datetime.html (bottom of the page)
    indatefmt = "%Y-%m-%d"
    
    
    # open the text file and read all lines into a variable "tmpdat"
    tmpdat = open(infile,'r').readlines()
    
    # make empty lists to temporarily hold the data
    Site_no = []
    dates = []
    DTW = []
    
    # loop over the input data, keep only proper data rows. Parse and assign to lists
    for line in tmpdat:
        if (('usgs' in line.lower()) and ('#' not in line)):
            tmp = line.strip().split() # strip newline off the end and split on whitespace
            Site_no.append(tmp[1])
            dates.append(datetime.strptime(tmp[2],indatefmt)) #convert date to a time tuple
            DTW.append(tmp[3])
    Site_no = np.array(Site_no,dtype=str) # convert to a numpy array
                                          # keep as str to not lose trailing zeroes (!)
    DTW = np.array(DTW,dtype=float) # convert to numpy array as a float containing the measurements
    dates = np.array(dates,dtype=object) #conver to numpy array as object since these are time tuples
    
    unique_sites = np.unique(Site_no) # get a unique list of the sites
    
    # make an empty dictionary to include the results
    indat = dict()
    # now loop over the unique sites and parse the results by site number
    for csite in unique_sites:
        cindices = np.nonzero(Site_no == csite)[0] # find the indices for the current site
        indat[csite] = {'dates':dates[cindices],'DTW':DTW[cindices]}
    return indat
   
def NWIS_plotter(indat,outplot,disp_plot):
    i=1
        
infile = 'dane_county_GW_wells.dat'
cdat = NWIS_reader(infile)
i=1