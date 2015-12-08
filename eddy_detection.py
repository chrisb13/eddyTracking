'''
Software for the tracking of eddies in OFAM model output following Chelton et al., Progress in Oceanography, 2011.

This is the first of two main scripts, namely:
    eddy_detection.py - detects the eddies
    eddy_tracking.py - examines output from eddy_detection.py and finds eddy tracks.

This script is normally run without arguments, unless using ./eddytrackwrap.py (see file for details.)

Usage:
    eddy_detection.py 
    eddy_detection.py --cli PCKLE_PATH
    eddy_detection.py -h
Options:
    -h,--help          : show this help message
    --cli PCKLE_PATH   : command line interface for eddytrackwrap.py, where PCKLE_PATH is a pickle containing the relevant details usually from experiments.py
'''

# Load required modules

import numpy as np

import matplotlib
# Turn the followin on if you are running on storm sometimes - Forces matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')


from matplotlib import pyplot as plt
import eddy_functions as eddy

import pickle
# Load parameters

import params
import experiments as exps

#for eddytrackwrap.py
from docopt import docopt
arguments = docopt(__doc__)
if arguments['--cli']:
    #load exps details from pickle...
    cli_exp_dict = pickle.load( open( arguments['--cli'], "rb" ) )

    exps.data_dir=cli_exp_dict['DATA_DIR']
    exps.dt=cli_exp_dict['DT']
    exps.pathroot=cli_exp_dict['PATHROOT']
    exps.plot_dir=cli_exp_dict['PLOT_DIR']
    exps.res=cli_exp_dict['RES']
    exps.run=cli_exp_dict['RUN']
    exps.T=cli_exp_dict['T']

    res_aviso = 0.25 # horizontal resolution of Aviso SSH fields [degrees]

    area_correction = res_aviso**2 / exps.res**2 # correction for different resoluttions of AVISO and OFAM
    exps.Npix_min = np.floor(8*area_correction) # min number of eddy pixels
    exps.Npix_max = np.floor(1000*area_correction) # max number of eddy pixels


# Load latitude and longitude vectors and restrict to domain of interest

lon, lat = eddy.load_lonlat(exps.run)

lon, lat, i1, i2, j1, j2 = eddy.restrict_lonlat(lon, lat, params.lon1, params.lon2, params.lat1, params.lat2)

# Loop over time

lon_eddies_a = []
lat_eddies_a = []
amp_eddies_a = []
area_eddies_a = []
scale_eddies_a = []
lon_eddies_c = []
lat_eddies_c = []
amp_eddies_c = []
area_eddies_c = []
scale_eddies_c = []

print 'eddy detection started'
print "number of time steps to loop over: ",exps.T
for tt in range(exps.T):
    print "timestep: ",tt+1,". out of: ", exps.T

    # Load map of sea surface height (SSH)
 
    eta, eta_miss = eddy.load_eta(exps.run, tt, i1, i2, j1, j2)
    eta = eddy.remove_missing(eta, missing=eta_miss, replacement=np.nan)
    #eddy.quick_plot(eta,findrange=True)
    # 
    ## Spatially filter SSH field
    # 
    eta_filt = eddy.spatial_filter(eta, lon, lat, exps.res, params.cut_lon, params.cut_lat)
    #eddy.quick_plot(eta_filt,findrange=True)
    # 
    ## Detect lon and lat coordinates of eddies
    #
    lon_eddies, lat_eddies, amp, area, scale = eddy.detect_eddies(eta_filt, lon, lat, params.ssh_crits, exps.res, exps.Npix_min, exps.Npix_max, params.amp_thresh, params.d_thresh, cyc='anticyclonic')
    lon_eddies_a.append(lon_eddies)
    lat_eddies_a.append(lat_eddies)
    amp_eddies_a.append(amp)
    area_eddies_a.append(area)
    scale_eddies_a.append(scale)

    lon_eddies, lat_eddies, amp, area, scale = eddy.detect_eddies(eta_filt, lon, lat, params.ssh_crits, exps.res, exps.Npix_min, exps.Npix_max, params.amp_thresh, params.d_thresh, cyc='cyclonic')
    lon_eddies_c.append(lon_eddies)
    lat_eddies_c.append(lat_eddies)
    amp_eddies_c.append(amp)
    area_eddies_c.append(area)
    scale_eddies_c.append(scale)
 
    # Plot map of filtered SSH field

    eddies_a=(lon_eddies_a[tt],lat_eddies_a[tt])
    eddies_c=(lon_eddies_c[tt],lat_eddies_c[tt])
    eddy.detection_plot(tt,lon,lat,eta,eta_filt,eddies_a,eddies_c,'rawtoo',exps.plot_dir,findrange=False)


# Combine eddy information from all days into a list

eddies = eddy.eddies_list(lon_eddies_a, lat_eddies_a, amp_eddies_a, area_eddies_a, scale_eddies_a, lon_eddies_c, lat_eddies_c, amp_eddies_c, area_eddies_c, scale_eddies_c)

np.savez(exps.data_dir+'eddy_det_'+exps.run, eddies=eddies)
