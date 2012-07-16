'''
Code to retrieve time series data from NWIS using a web service

'''
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42

# using County Codes
example_url_1 = "http://waterservices.usgs.gov/nwis/dv/?format=rdb&countyCd=55025&startDT=1959-01-01&endDT=2012-07-16&siteType=GW"
# using SiteID Codes
example_url_2 = "http://waterservices.usgs.gov/nwis/dv/?format=rdb,1.0&sites=430406089232901,430427089284901&startDT=1959-01-01&endDT=2012-07-16&parameterCd=72019&siteType=GW"
Sites = [430406089232901,430427089284901]
