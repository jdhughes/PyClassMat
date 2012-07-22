'''
NWIS_web_puller()
A coad to download an NWIS file using USGS webservices.
Mike Fienen - 7/16/2012
<mnfienen *at* usgs *dot* gov>

INPUT:
none--> user is prompted for all input
OUTPUT:
none--> a text file is written by the USGS weservices with a name
        specified by the user
'''
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42
import os
import NWIS_read_pars as NWR

# ############
# function definitions
# ############


# Function to query NWIS with a list of station numbers
def retrieve_by_stations(cStations,sttime,endtime,outfilename):
    print 'Pulling data for list of stations'
    urlParts = ['http://waterservices.usgs.gov/nwis/dv/?format=rdb,1.0&sites=',
                '&startDT=',
                '&endDT=',
                '&parameterCd=72019&siteType=GW']
    fullURL = urlParts[0] 
    for i,cs in enumerate(cStations):
        fullURL += cs
        if i < len(cStations):
            fullURL += ','
    fullURL += urlParts[1] + sttime + urlParts[2] + endtime + urlParts[3]
    datastream = urllib.urlopen(fullURL).read()
    open(outfilename,'wb').write(datastream)
    
# Function to query NWIS for all the wells in a State County combination     
def retrieve_by_state_county(cState,cCounty,sttime,endtime,outfilename):
    state_lookup_full,state_lookup_abbrev,county_lookup = read_state_county_FIPS()    
    urlParts = ['http://waterservices.usgs.gov/nwis/dv/?format=rdb&countyCd=',
            '&startDT=',
            '&endDT=',
            '&parameterCd=72019&siteType=GW']
    fullURL = urlParts[0] + cState + cCounty + urlParts[1] + sttime + urlParts[2] + endtime + urlParts[3]
    datastream = urllib.urlopen(fullURL).read()
    open(outfilename,'wb').write(datastream)
    

# ######## # 
 #  M A I N #
  # ######## # 
print 'You are about to enter the NWIS puller zone\nReady?\n\n'

stat_county = raw_input('Would you like to query by Station Numbers [stat] or County and State [count]?:')

if stat_county.lower() == 'count':
    cState = raw_input('Please enter state as full, abbreviated, or FIPS code:')
    cCounty = raw_input('Please enter county name or FIPS code\ninclude "county", "parish", etc:')
    sttime = raw_input('Please enter start date in format "YYYY-MM-DD":')
    endtime = raw_input('Please enter end date in format "YYYY-MM-DD":')
    outfilename = raw_input('Please enter a filename for your results:')
    retrieve_by_state_county(cState,cCounty,sttime,endtime,outfilename)
elif stat_county.lower() == 'stat':
    tmp_input = raw_input('Please enter 14-digit station codes, separated by commas:')
    sttime = raw_input('Please enter start date in format "YYYY-MM-DD":')
    endtime = raw_input('Please enter end date in format "YYYY-MM-DD":')
    outfilename = raw_input('Please enter a filename for your results:')
    tmp = tmp_input.split(',')
    cStations = []
    for i in tmp:
        cStations.append(i)
    retrieve_by_stations(cStations,sttime,endtime,outfilename)
else:
    print 'Invalid state or county selection'
    exit







