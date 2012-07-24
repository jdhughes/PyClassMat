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
import NWIS_read_parse as NWR
import urllib


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
        if i+1 < len(cStations):
            fullURL += ','
    fullURL += urlParts[1] + sttime + urlParts[2] + endtime + urlParts[3]
    print 'Using URL:\n%s' %(fullURL)
    datastream = urllib.urlopen(fullURL).read()
    open(outfilename,'wb').write(datastream)
    print 'File download complete'
    print 'output written to %s' %(outfilename)
    
# Function to query NWIS for all the wells in a State County combination     
def retrieve_by_state_county(cState,cCounty,sttime,endtime,outfilename,stat_county):
    if stat_county == 'county':
        print 'Pulling data for %s in %s' %(cCounty, cState)
    elif stat_county == 'state':
        print 'Pulling data for %s' %(cState)
    state_lookup_full,state_lookup_abbrev,county_lookup,state_full_abbrev_lookup = NWR.read_state_county_FIPS()    
    stateFIPS,countyFIPS = NWR.get_county_and_state_FIPS(cState,cCounty,state_lookup_full,state_lookup_abbrev,county_lookup)
    urlParts = ['http://waterservices.usgs.gov/nwis/dv/?format=rdb',
            '&countyCd=',
            '&stateCd=',
            '&startDT=',
            '&endDT=',
            '&parameterCd=72019&siteType=GW']
    if stat_county == 'county':
        fullURL = urlParts[0] + urlParts[1] + stateFIPS + countyFIPS + urlParts[3] + sttime + urlParts[4] + endtime + urlParts[5]
    elif stat_county == 'state':
        if len(cState) > 2:
            cState = state_lookup_abbrev[cState]
        fullURL = urlParts[0] + urlParts[2] + cState + urlParts[3] + sttime + urlParts[4] + endtime + urlParts[5]
        
    print 'Using URL:\n%s' %(fullURL)
    datastream = urllib.urlopen(fullURL).read()
    open(outfilename,'wb').write(datastream)
    print 'File download complete'    
    print 'output written to %s' %(outfilename)

# ######## # 
 #  M A I N #
  # ######## # 
def Web_pull_driver():
    print 'You are about to enter the NWIS puller zone\nReady?\n\n'
    
    stat_county = raw_input('Would you like to query by Station Numbers [station] \nState [state], or County and State [county]?:')
    
    if stat_county.lower() == 'county' or stat_county.lower() == 'state':
        cState = raw_input('Please enter state as full, abbreviated, or FIPS code:')
        if stat_county.lower() == 'county':
            cCounty = raw_input('Please enter county name or FIPS code\ninclude "county", "parish", etc:')
        else:
            cCounty = '999999'
        sttime = raw_input('Please enter start date in format "YYYY-MM-DD":')
        endtime = raw_input('Please enter end date in format "YYYY-MM-DD":')
        outfilename = raw_input('Please enter a filename for your results:')
        retrieve_by_state_county(cState,cCounty,sttime,endtime,outfilename,stat_county.lower())
    elif stat_county.lower() == 'stat':
        tmp_input = raw_input('Please enter 15-digit station codes, separated by commas:')
        sttime = raw_input('Please enter start date in format "YYYY-MM-DD":')
        endtime = raw_input('Please enter end date in format "YYYY-MM-DD":')
        outfilename = raw_input('Please enter a filename for your results:')
        tmp = tmp_input.split(',')
        cStations = []
        for i in tmp:
            cStations.append(i)
        retrieve_by_stations(cStations,sttime,endtime,outfilename)
    else:
        print 'Invalid station, state, or county selection'
    return outfilename
    
    
    
    
    
    
    
