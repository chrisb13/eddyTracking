
# Automated eddy detection
 
Eric Oliver

Code for the detection and tracking of eddies, following Chelton et al. (Prog. Ocean., 2011) given a series of sea level maps.

Code Description
============                     

File                 |Description
---------------------|----------
|eddy_detection.py    | Code for the detection of eddies given a series of sea level maps|
|eddy_tracking.py     | Code for the tracking of eddies after detection has been performed|
|params.py            | Parameter file used by eddy detection and eddy tracking programs|
|find_T.py            | Added by Chris, support file for params.py for NEMO output to calculate how many timesteps in an experiment|
|eddy_census.py       | Code for calculating census statistics of tracked eddies|
|eddy_plot.py         | Code for plotting eddy tracks|
|eddy_functions.py    | Module of supporting functions|
|eddytrackwrap.py     | eddy_detection.py and eddy_tracking.py can now be run from a single interface via the command line. This does not run the plotting scripts. This is so the eddy tracking can be run on many NEMO experiments. Be aware that if you additional steps, e.g. eddy_tracking_two.py then you'll need to look at the import experiments steps in eddy_detection and eddy_tracking.|
| experiments.py      | Added by Chris, pertinent experiment information, separated from params as it may be modified by eddytrackwrap.py|

## Notes

1. This code as been applied to model output from OFAM  and from weekly and daily sea level maps from Aviso. To apply it to another dataset it is necessary to make the following adjustments:

 a. Add a new dataset id 'NAME' in the conditionals in params.py, including relevant parameters (number of time steps, resolution, time step).

 b. Add appropriate code in 'load_lonlat' and 'load_eta' functions (both in eddy_functions.py) to properly handle the loading of your data. Code assumes one file (spatial map) per time step.

1. rosrad.dat obtained from [here](http://www-po.coas.oregonstate.edu/research/po/research/rossby_radius/index.html). Specifically:
```bash
wget http://www-po.coas.oregonstate.edu/research/po/research/rossby_radius/rossrad.dat
```

## Changes added by Christopher Bull (Dec 2015)

Modified to work with NEMO. Made some general changes including:

 1. Works with python netCDF4 library.
 1. Refactored so global data and plot dirs are defined in params.py (and created if they don't exist)
 1. Refactored so that pathroot for input data can be defined in params rather than eddy_functions.
 1. Added quick_plot and detection_plot functions to eddy_function.py
 1. Added functions from ecoliver (that were not previously included) into eddy_functions.py
 1. Added rossrad.dat (and details on where it came from).
 1. Added eddytrackwrap.py so that eddy_detection.py and eddy_tracking.py can be run from a single interface via the command line (passing interface added). This does not run the plotting scripts. This is so the eddy tracking can be run on many NEMO experiments. Note the less than ideal way variables from experiments.py are modified.

Despite the new eddytrackwrap workflow, the scripts should still be able to run as ECJ described (notes above).

## Contact                                                                                                          
Eric C. J. Oliver                                                                                                                   
Institute for Marine and Antarctic Studies                                                                                          
University of Tasmania                                                                                                              
Hobart TAS, Australia
e: eric.oliver@utas.edu.au                                                                                                          
w: http://passage.phys.ocean.dal.ca/~olivere                                                                                   
https://github.com/ecjoliver 


Christopher Bull.                                                                                                                   
Climate Change Research Centre and ARC Centre of Excellence for Climate System Science.
University of New South Wales                                                                                                      
Sydney, NSW, Australia, 2052     
e: z3457920@student.unsw.edu.au                                                                                                    
w: christopherbull.com.au
github.com/chrisb13

t: @ChrisBullOceanO
