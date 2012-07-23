import numpy as np
import NWIS_read_parse as NWR


# get the FIPS codes lookups for states and counties
a,b,c = NWR.read_state_county_FIPS()

# now find the specific code for place of interst
cS = 'WI'
cC = 'Dane County'
sF,cF = NWR.get_county_and_state_FIPS(cS,cC,a,b,c)

# example using a static file already in place

infile = 'dane_county_GW_wells.dat'
cdat,station_lookup = NWR.NWIS_reader(infile)

NWR.NWIS_plotter(cdat,station_lookup,'.png')

