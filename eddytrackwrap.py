#   Author: Christopher Bull. 
#   Affiliation: Climate Change Research Centre and ARC Centre of Excellence for Climate System Science.
#                Level 4, Mathews Building
#                University of New South Wales
#                Sydney, NSW, Australia, 2052
#   Contact: z3457920@student.unsw.edu.au
#   www:     christopherbull.com.au
#   Date created: Tue, 08 Dec 2015 11:53:37
#   Machine created on: ccrc165
#

"""
Main function to automate NEMO eddy tracking for the following files:
    ./eddy_detection.py
    ./eddy_tracking.py

Interface is by command line.

Usage:
    eddytrackwrap.py 
    eddytrackwrap.py -h
    eddytrackwrap.py RUN RES DT PATHROOT DATA_DIR PLOT_DIR
Options:
    -h,--help          : show this help message
    RUN                : Run Name
    RES                : run horizontal resolution of SSH field [degrees]
    DT                 : Sample rate of detected eddies [days]
    PATHROOT           : path to data
    DATA_DIR           : path to put all our working data in
    PLOT_DIR           : path to put all our plots in

Notes:
    Will determine the number of time steps (T) automatically!

Example:
python eddytrackwrap.py 'cb_NEMO' 0.25 1 '/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/' ./ ./
python eddytrackwrap.py 'cb_NEMO' 0.25 1 /home/chris/codescratch/mkmov/ ./ ./
"""

#see: https://github.com/docopt/docopt
#round brackets mean required square are optional

#download docopt from...
#https://raw.githubusercontent.com/docopt/docopt/master/docopt.py
from docopt import docopt

# import tempfile
# workingfol=tempfile.mkdtemp()+'/'
import subprocess
import pickle

#just so we can find the number of time steps our NEMO experiment has
from eddy_functions import raw_nemo_globber_specifytpe

#is this needed?
import pandas as pd

def find_T(path_to_experiment):
    """function to find the number of time steps for a NEMO experiment, as files contain different numbers of time steps.

    :path_to_experiment: path to experiment that was passed into this file
    :returns: number of time steps (int dtype)
    """
    return len(raw_nemo_globber_specifytpe(path_to_experiment,return_dates=True))

    pass

if __name__ == "__main__": 
    #read in/process  arguments
    arguments = docopt(__doc__)

    # print arguments
    workingfolder=arguments['DATA_DIR']

    #change dtype from string
    arguments['DT']=float(arguments['DT'])
    arguments['RES']=float(arguments['RES'])

    #grab the number of time steps we'll be cycling through
    arguments['T']=find_T(arguments['PATHROOT'])

    #Save a dictionary into a pickle file.
    pickle.dump( arguments, open( workingfolder+'pickleargs.p', "wb" ) )

    subprocess.call('python eddy_detection.py --cli '+\
        workingfolder+'pickleargs.p',shell=True)

    subprocess.call('python eddy_tracking.py --cli '+\
        workingfolder+'pickleargs.p',shell=True)
