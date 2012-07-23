import numpy as np
import NWIS_read_parse as NWR
import NWIS_web_puller as NWISWebPull

testCase = 2

if testCase == 1:
    #
    # JUST RUN THROUGH THE NWIS_read_parse functions
    #
    
    # get the FIPS codes lookups for states and counties
    state_lookup_full,state_lookup_abbrev,county_lookup,state_abbrev_full = NWR.read_state_county_FIPS()
    
    # now find the specific code for place of interst
    cState = 'WI'
    cCounty = 'Dane County'
    sFIPS,cFIPS = NWR.get_county_and_state_FIPS(cState,cCounty,state_lookup_full,
                                                state_lookup_abbrev,county_lookup)

    print 'FIPS code for %s is %s\nFIPS code for %s is %s' %(cState,sFIPS,cCounty,cFIPS)
if testCase == 2:
    #
    # RUN THROUGH THE DIALOGUE OF PULLING RECORDS AND USE THE OUTPUT FILE TO PARSE AND PLOT
    #
    
    infile = NWISWebPull.Web_pull_driver()
    # example using a static file already in place
    
    cdat,station_lookup = NWR.NWIS_reader(infile)
    
    NWR.NWIS_plotter(cdat,station_lookup,'.png')

    print " All done! Check the 'figures' subdirectory for your plotted results"