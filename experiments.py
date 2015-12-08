"""
List of experiments and their associated settings

These settings have been split off from params.py so they can be controlled with argpassing, see ./eddytrackwrap.py for details.
"""
import numpy as np

###############
#  CHANGE ME  #
###############

NAME = 'cb_NEMO' # Which dataset/model run for which to detect eddies (AVISO, CTRL or A1B)

###############
#  CHANGE ME  #
###############

def mkdir(p):
    """make directory of path that is passed"""
    import os
    try:
       os.makedirs(p)
       print "output folder: "+p+ " does not exist, we will make one."
    except OSError as exc: # Python >2.5
       import errno
       if exc.errno == errno.EEXIST and os.path.isdir(p):
          pass
       else: raise

#working folder
data_dir = '/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking2/'
data_dir = './'
plot_dir = './'
plot_dir = data_dir + 'plots/'
mkdir(data_dir)
mkdir(plot_dir)

if NAME == 'CTRL':
    run = NAME
    T = 9*365 # Number of time steps to loop over
    res = 0.1 # horizontal resolution of SSH field [degrees]
    dt = 1. # Sample rate of detected eddies [days]
elif NAME == 'A1B':
    run = NAME
    T = 9*365 # Number of time steps to loop over
    res = 0.1 # horizontal resolution of SSH field [degrees]
    dt = 1. # Sample rate of detected eddies [days]
elif NAME == 'AVISO':
    run = NAME
    T = 876 # Number of time steps to loop over
    res = 0.25 # horizontal resolution of SSH field [degrees]
    dt = 7. # Sample rate of detected eddies [days]
elif NAME == 'AVISOd':
    run = NAME
    T = 7967 # Number of time steps to loop over
    res = 0.25 # horizontal resolution of SSH field [degrees]
    dt = 1. # Sample rate of detected eddies [days]
elif NAME == 'cb_AVISO':
    run = NAME
    T = 4 # Number of time steps to loop over
    res = 0.25 # horizontal resolution of SSH field [degrees]
    dt = 1. # Sample rate of detected eddies [days]
    pathroot='/srv/ccrc/data42/z3457920/RawData/AVISO/RawData/dt_global_allsat_madt/ftp.aviso.altimetry.fr/global/delayed-time/grids/madt/all-sat-merged/h/1993/'
elif NAME == 'cb_NEMO':
    run = NAME
    #T = 365 # Number of time steps to loop over

    #do the following to find T
    #python find_T
    T=7670 # Number of time steps to loop over
    T=5 # Number of time steps to loop over

    res = 0.25 # horizontal resolution of SSH field [degrees]
    dt = 1. # Sample rate of detected eddies [days]
    pathroot='/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/'


res_aviso = 0.25 # horizontal resolution of Aviso SSH fields [degrees]

area_correction = res_aviso**2 / res**2 # correction for different resoluttions of AVISO and OFAM
Npix_min = np.floor(8*area_correction) # min number of eddy pixels
Npix_max = np.floor(1000*area_correction) # max number of eddy pixels

