'''
Software for the tracking of eddies in OFAM model output following Chelton et al., Progress in Oceanography, 2011.

This is the first of two main scripts, namely:
    eddy_detection.py - detects the eddies
    eddy_tracking.py - examines output from eddy_detection.py and finds eddy tracks.

This script is normally run without arguments, unless using ./eddytrackwrap.py (see file for details.)

Usage:
    eddy_tracking.py 
    eddy_tracking.py --cli PCKLE_PATH
    eddy_tracking.py -h
Options:
    -h,--help          : show this help message
    --cli PCKLE_PATH   : command line interface for eddytrackwrap.py, where PCKLE_PATH is a pickle containing the relevant details usually from experiments.py
'''
# Load required modules

import numpy as np
import eddy_functions as eddy

import pickle
# Load parameters

import params
import experiments as exps

getNEMOtime=False

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
    # exps.T=3 #TEMP TEP

    res_aviso = 0.25 # horizontal resolution of Aviso SSH fields [degrees]

    area_correction = res_aviso**2 / exps.res**2 # correction for different resoluttions of AVISO and OFAM
    exps.Npix_min = np.floor(8*area_correction) # min number of eddy pixels
    exps.Npix_max = np.floor(1000*area_correction) # max number of eddy pixels

    getNEMOtime=True

# Automated eddy tracking

data = np.load(exps.data_dir+'eddy_det_'+exps.run+'.npz')
det_eddies = data['eddies'] # len(eddies) = number of time steps

# Initialize eddies discovered at first time step

eddies = eddy.eddies_init(det_eddies)

# Stitch eddy tracks together at future time steps

print 'eddy tracking started'
print "number of time steps to loop over: ",exps.T

rossrad = eddy.load_rossrad() # Atlas of Rossby radius of deformation and first baroclinic wave speed (Chelton et al. 1998)

#grab NEMO timesteps
if getNEMOtime:
    nemo_tsteps=eddy.load_nemo_time()

for tt in range(1, exps.T):

    print "timestep: " ,tt+1,". out of: ", exps.T

    # Track eddies from time step tt-1 to tt and update corresponding tracks and/or create new eddies

    eddies = eddy.track_eddies(eddies, det_eddies, tt, exps.dt, params.dt_aviso, params.dE_aviso, rossrad, params.eddy_scale_min, params.eddy_scale_max)

    if not getNEMOtime:
        # Save data incrementally

        if( np.mod(tt, params.dt_save)==0 ):

            np.savez(exps.data_dir+'eddy_track_'+exps.run, eddies=eddies)

# Add keys for eddy age and flag if eddy was still in existence at end of exps.run

for ed in range(len(eddies)):

    eddies[ed]['age'] = len(eddies[ed]['lon'])

if getNEMOtime:
    eddies=eddy.add_time_2tracked_eddies(eddies, nemo_tsteps)

np.savez(exps.data_dir+'eddy_track_'+exps.run, eddies=eddies)
