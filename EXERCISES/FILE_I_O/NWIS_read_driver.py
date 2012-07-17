import numpy as np
import NWIS_read_parse as NWR

# example using a static file already in place
infile = 'dane_county_GW_wells.dat'
cdat,station_lookup = NWR.NWIS_reader(infile)

NWR.NWIS_plotter(cdat,station_lookup,'.png')

i=1