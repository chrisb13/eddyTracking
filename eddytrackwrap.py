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
    eddytrackwrap.py RUN RES DT PATHROOT DATA_DIR PLOT_DIR [--mc MCORE] 
Options:
    -h,--help          : show this help message
    RUN                : Run Name
    RES                : run horizontal resolution of SSH field [degrees]
    DT                 : Sample rate of detected eddies [days]
    PATHROOT           : path to data
    DATA_DIR           : path to put all our working data in
    PLOT_DIR           : path to put all our plots in
    --mc MCORE         : str with 'corenumber'+'_'+'number-of-cores' 

Notes:
    Will determine the number of time steps (T) automatically!

Example:
python eddytrackwrap.py 'cb_NEMO' 0.25 1 '/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/' ./ ./
python eddytrackwrap.py 'cb_NEMO' 0.25 1 /home/chris/codescratch/mkmov/ ./ ./

python /home/z3457920/hdrive/repos/nemo_analysis/diagnostics/eddytracking/eddytrackwrap.py 'cb_NEMO' 0.25 1 /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24_ERAI01/plots/ 
python /home/z3457920/hdrive/repos/nemo_analysis/diagnostics/eddytracking/eddytrackwrap.py 'cb_NEMO' 0.25 1 /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01b/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24_ERAI01b/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24_ERAI01b/plots/ 
python /home/z3457920/hdrive/repos/nemo_analysis/diagnostics/eddytracking/eddytrackwrap.py 'cb_NEMO' 0.25 1 /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24REALNONZ500_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24REALNONZ500_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24REALNONZ500_ERAI01/plots/ 
python /home/z3457920/hdrive/repos/nemo_analysis/diagnostics/eddytracking/eddytrackwrap.py 'cb_NEMO' 0.25 1 /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24REALNONZ80_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24REALNONZ80_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24REALNONZ80_ERAI01/plots/ 
python /home/z3457920/hdrive/repos/nemo_analysis/diagnostics/eddytracking/eddytrackwrap.py 'cb_NEMO' 0.25 1 /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24FBCTRL_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24FBCTRL_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24FBCTRL_ERAI01/plots/ 
python /home/z3457920/hdrive/repos/nemo_analysis/diagnostics/eddytracking/eddytrackwrap.py 'cb_NEMO' 0.25 1 /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24FBNONZ4000_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24FBNONZ4000_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24FBNONZ4000_ERAI01/plots/ 
python /home/z3457920/hdrive/repos/nemo_analysis/diagnostics/eddytracking/eddytrackwrap.py 'cb_NEMO' 0.25 1 /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24SLGEOV1_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24SLGEOV1_ERAI01/ /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking/nemo_cordex24SLGEOV1_ERAI01/plots/ 
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

import os

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

def find_T(path_to_experiment):
    """function to find the number of time steps for a NEMO experiment, as files contain different numbers of time steps.

    :path_to_experiment: path to experiment that was passed into this file
    :returns: number of time steps (int dtype)
    """
    return len(raw_nemo_globber_specifytpe(path_to_experiment,return_dates=True))

    pass

if __name__ == "__main__": 
    print "Running Eddy Tracker in arg passing mode!"
    #read in/process  arguments
    arguments = docopt(__doc__)

    print arguments
    # import pdb; pdb.set_trace()
    workingfolder=arguments['DATA_DIR']

    print "Creating/checking we have output dirs."
    mkdir(arguments['DATA_DIR'])
    mkdir(arguments['PLOT_DIR'])

    #change dtype from string
    arguments['DT']=float(arguments['DT'])
    arguments['RES']=float(arguments['RES'])

    #grab the number of time steps we'll be cycling through
    arguments['T']=find_T(arguments['PATHROOT'])

    #Save a dictionary into a pickle file.
    pickle.dump( arguments, open( workingfolder+'pickleargs.p', "wb" ) )
    print "dumping arguments into pickle here: "+workingfolder+'pickleargs.p'

    if arguments['--mc'] is not None:
        print "Running Eddy Tracker in multi_core mode!"
        # corenum=arguments['--mc'].split('_')[0]
        # coretotal=arguments['--mc'].split('_')[1]
        # print corenum, coretotal
        subprocess.call('python '+os.path.dirname(os.path.realpath(__file__))+ '/eddy_detection.py --cli '+workingfolder+'pickleargs.p'+\
                ' --mc ' + arguments['--mc']\
                ,shell=True)
    else:
        print "executing: "+'python '+os.path.dirname(os.path.realpath(__file__))+ '/eddy_detection.py --cli '+workingfolder+'pickleargs.p'
        subprocess.call('python '+os.path.dirname(os.path.realpath(__file__))+ '/eddy_detection.py --cli '+workingfolder+'pickleargs.p',shell=True)

        print "executing: "+'python '+os.path.dirname(os.path.realpath(__file__))+ '/eddy_tracking.py --cli '+workingfolder+'pickleargs.p'
        subprocess.call('python '+os.path.dirname(os.path.realpath(__file__))+ '/eddy_tracking.py --cli '+workingfolder+'pickleargs.p',shell=True)
